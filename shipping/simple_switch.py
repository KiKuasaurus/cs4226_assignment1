# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types


class SimpleSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch, self).__init__(*args, **kwargs)
        # A in-memory mac to port matching on the controller side
        self.mac_to_port = {}

    # CHECK_THIS_OUT
    # https://ryu.readthedocs.io/en/latest/ofproto_v1_3_ref.html#ryu.ofproto.ofproto_v1_3_parser.OFPSwitchFeatures
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        # CHECK_THIS_OUT
        # https://ryu.readthedocs.io/en/latest/ryu_app_api.html#ryu-controller-controller-datapath
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        # If a packet does not match any flow on the switch
        # Send it to the controller for processing
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        # CHECK_THIS_OUT
        # https://ryu.readthedocs.io/en/latest/ofproto_v1_3_ref.html#ryu.ofproto.ofproto_v1_3_parser.OFPFlowMod
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id and (not buffer_id==ofproto.OFP_NO_BUFFER):
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # get the datapath (i.e. switch) related
        # and the port where the packet came in from
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        # Get the packet the switch received
        # from the message sent by the switch to the controller
        pkt = packet.Packet(msg.data)
        # Get ethernet frame
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        # ignore lldp packet
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        # TODO: Add a MAC-to-port mapping between the source mac address and income port
        # to the in-memory dictionary (self.mac_to_port)
        self.mac_to_port[dpid][src] = in_port

        # TODO: check if there is an entry corresponding to the destination mac in self.mac_to_port
        # Set the output port accordingly if yes, set output port to flood if none
        # CHECK_THIS_OUT (pay attention to the example)
        # https://ryu.readthedocs.io/en/latest/ofproto_v1_3_ref.html#ryu.ofproto.ofproto_v1_3_parser.OFPPacketOut
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        # TODO: create a list of actions that instructs the switch to forward the packet to the output port
        actions = [parser.OFPActionOutput(out_port, 0)]
        
        # TODO: check if the output port is flood
        # if not flooded
        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:

        # TODO: create an OFPMatch instance to match all the packets
        # with (ethernet source address==src AND ethernet destination address==dst AND received from in_port)
        # use self.add_flow()
        # CHECK_THIS_OUT
        # https://ryu.readthedocs.io/en/latest/ofproto_v1_3_ref.html#ryu.ofproto.ofproto_v1_3_parser.OFPMatch
            ofp_match = parser.OFPMatch(eth_src=src, eth_dst=dst, in_port=in_port)

            self.add_flow(
                datapath= datapath,
                priority= 1,
                match= ofp_match,
                actions= actions
            )
        
        # TODO: Send the packet out message for the current packet if the packet is not buffered on the switch
        # check if msg.buffer_id is ofproto.OFP_NO_BUFFER
        # If yes an OFPPacketOut message must be sent to the switch to forward the current packet
        # Otherwise nothing needs to be done since the the switch has buffered the packet 
        # and it will automatically forward it according to the flow rule just installed
        # CHECK_THIS_OUT
        # https://ryu.readthedocs.io/en/latest/ofproto_v1_3_ref.html#ryu.ofproto.ofproto_v1_3_parser.OFPPacketOut
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            req = parser.OFPPacketOut(datapath, msg.buffer_id, 
                                          in_port, actions, msg.data)
            datapath.send_msg(req)
        
