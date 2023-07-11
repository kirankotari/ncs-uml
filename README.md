# NCS-UML

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-yellow)](https://opensource.org/license/apache-2-0/)
[![Downloads](https://pepy.tech/badge/ncs-uml)](https://pepy.tech/project/ncs-uml)
[![GitHub issues open](https://img.shields.io/github/issues/kirankotari/ncs-uml.svg?)](https://github.com/kirankotari/ncs-uml/issues)

- [Introduction](#introduction)
- [Commands](#commands)
- [Documentation](#docs)
- [Pre-requisites](#pre-requisites)
- [Installation and Downloads](#installation-and-downloads)
- [FAQ](#faq)
- [Bug Tracker and Support](#bug-tracker-and-support)
- [License and Copyright](#license-and-copyright)
- [Author and Thanks](#author-and-thanks)

## Introduction

A Python library and CLI tool that generates plantUML code from the given input YANG Model file. It grabs the dependencies yang models from the Makefile and from NCS. 

To generate a png image or a svg file, install plantUML plugin for VSCode or other editors. plantUML has the web editor available at [plantuml.com](http://www.plantuml.com/)

## Commands

```sh
Usage: ncs-uml [options] [<filename>...]

Creates plantUML file for the YANG module in <filename>, and all its dependencies.
It can be converted into PNG/SVG images using www.plantuml.com or with editor plugins.

Options:
  -h, --help            Show this help message and exit
  -v, --version         Show version number and exit
  -V, --verbose
  --no-inline-groupings
  --dependent-yang-paths=DEPENDENT_YANG_PATHS
                        dependent yang module paths
  --no-inline-groupings-from=NO_INLINE_GROUPINGS_FROM
                        Skips given modules from inline groupings.  Example
                        --uml-no-inline-groupings-from=ietf-yang-push
  --add-legend          Adds legend about grouping yang file in the UML
```

## Docs

**How to use ncs-uml?**

- Command Line  
  Type `ncs-uml <YangFile>`. For more help type `ncs-uml --help`

```shell
user$ ncs-uml $NCS_DIR/examples.ncs/getting-started/developing-with-ncs/17-mpls-vpn-python/packages/l3vpn/src/yang/l3vpn.yang --no-inline-groupings-from=tailf-ncs --add-legend
 INFO |   main | uml file: l3vpn.uml
 INFO |   main | uml clean up done.
user$
```

It returns plantUML code, which can easily converted to image.

![l3vpn](l3vpn.png)

Plant UML code:
```plantuml.server
@startuml l3vpn
hide empty fields 
hide empty methods 
hide <<case>> circle
hide <<augment>> circle
hide <<choice>> circle
hide <<leafref>> stereotype
hide <<leafref>> circle
page 1x1 
Title l3vpn 
class "l3vpn" as l3vpn << (M, #33CCFF) module>> 
class "dscp-type" as dscp_type << (T, YellowGreen) typedef>>
dscp_type : union{uint16, enumeration}
enum "protocol-type" as l3vpn_I_protocol_type {
icmp
igmp
ipip
MORE
}
class "qos-match-type" as qos_match_type << (T, YellowGreen) typedef>>
qos_match_type : union{tailf:ipv4-address-and-prefix-length, enumeration}
class "topology" as  l3vpn_I_topology <<container>> 
l3vpn *-- "1" l3vpn_I_topology 
class "role" as l3vpn_I_topology_I_role << (L, #FF7700) list>> 
l3vpn_I_topology *-- "0..N" l3vpn_I_topology_I_role 
l3vpn_I_topology_I_role : +role : enumeration : {ce,pe,p,}  {key} 
l3vpn_I_topology_I_role : device []: leafref : /ncs:devices/ncs:device/ncs:name 
class "connection" as l3vpn_I_topology_I_connection << (L, #FF7700) list>> 
l3vpn_I_topology *-- "0..N" l3vpn_I_topology_I_connection 
l3vpn_I_topology_I_connection : +name : string  {key} 
class "endpoint-1" as  l3vpn_I_topology_I_connection_I_endpoint_1 <<container>> 
l3vpn_I_topology_I_connection *-- "1" l3vpn_I_topology_I_connection_I_endpoint_1 
l3vpn_I_topology_I_connection_I_endpoint_1 : device : leafref : /ncs:devices/ncs:device/ncs:name  
l3vpn_I_topology_I_connection_I_endpoint_1 : interface : string  
l3vpn_I_topology_I_connection_I_endpoint_1 : ip-address : tailf:ipv4-address-and-prefix-length  
class "endpoint-2" as  l3vpn_I_topology_I_connection_I_endpoint_2 <<container>> 
l3vpn_I_topology_I_connection *-- "1" l3vpn_I_topology_I_connection_I_endpoint_2 
l3vpn_I_topology_I_connection_I_endpoint_2 : device : leafref : /ncs:devices/ncs:device/ncs:name  
l3vpn_I_topology_I_connection_I_endpoint_2 : interface : string  
l3vpn_I_topology_I_connection_I_endpoint_2 : ip-address : tailf:ipv4-address-and-prefix-length  
l3vpn_I_topology_I_connection : link-vlan : uint32  
class "qos" as  l3vpn_I_qos <<container>> 
l3vpn *-- "1" l3vpn_I_qos 
class "qos-policy" as l3vpn_I_qos_I_qos_policy << (L, #FF7700) list>> 
l3vpn_I_qos *-- "0..N" l3vpn_I_qos_I_qos_policy 
l3vpn_I_qos_I_qos_policy : +name : string  {key} 
class "class" as l3vpn_I_qos_I_qos_policy_I_class << (L, #FF7700) list>> 
l3vpn_I_qos_I_qos_policy *-- "0..N" l3vpn_I_qos_I_qos_policy_I_class 
l3vpn_I_qos_I_qos_policy_I_class : +qos-class : leafref : /qos/qos-class/name  {key} 
l3vpn_I_qos_I_qos_policy_I_class : bandwidth-percentage : uint32  
l3vpn_I_qos_I_qos_policy_I_class : priority : empty  
class "qos-class" as l3vpn_I_qos_I_qos_class << (L, #FF7700) list>> 
l3vpn_I_qos *-- "0..N" l3vpn_I_qos_I_qos_class 
l3vpn_I_qos_I_qos_class : +name : string  {key} 
l3vpn_I_qos_I_qos_class : dscp-value : dscp-type  
class "match-traffic" as l3vpn_I_qos_I_qos_class_I_match_traffic << (L, #FF7700) list>> 
l3vpn_I_qos_I_qos_class *-- "0..N" l3vpn_I_qos_I_qos_class_I_match_traffic 
l3vpn_I_qos_I_qos_class_I_match_traffic : +name : string  {key} 
l3vpn_I_qos_I_qos_class_I_match_traffic : source-ip : qos-match-type  
l3vpn_I_qos_I_qos_class_I_match_traffic : destination-ip : qos-match-type  
l3vpn_I_qos_I_qos_class_I_match_traffic : port-start : inet:port-number  
l3vpn_I_qos_I_qos_class_I_match_traffic : port-end : inet:port-number  
l3vpn_I_qos_I_qos_class_I_match_traffic : protocol : protocol-type  
class "vpn" as  l3vpn_I_vpn <<container>> 
l3vpn *-- "1" l3vpn_I_vpn 
class "l3vpn" as l3vpn_I_vpn_I_l3vpn << (L, #FF7700) list>> 
l3vpn_I_vpn *-- "0..N" l3vpn_I_vpn_I_l3vpn 
l3vpn_I_vpn_I_l3vpn : +name : string  {key} 
l3vpn_I_vpn_I_l3vpn : callpoint:ncs-rfs-service-hook()
l3vpn_I_vpn_I_l3vpn : check-sync( in: outformat in: suppress_positive_result in: service_depth in: choice_lsa_grouping)
l3vpn_I_vpn_I_l3vpn : deep-check-sync( in: outformat in: suppress_positive_result in: choice_lsa_grouping in: wait_for_lock)
l3vpn_I_vpn_I_l3vpn : re-deploy( in: dry_run in: reconcile in: ncs_commit_params in: service_depth out: ncs_commit_result)
l3vpn_I_vpn_I_l3vpn : reactive-re-deploy( in: sync out: ncs_commit_result)
l3vpn_I_vpn_I_l3vpn : touch()
class "modified" as  l3vpn_I_vpn_I_l3vpn_I_modified <<container>> 
l3vpn_I_vpn_I_l3vpn *-- "1" l3vpn_I_vpn_I_l3vpn_I_modified 
l3vpn_I_vpn_I_l3vpn_I_modified : callpoint:ncs()
l3vpn_I_vpn_I_l3vpn_I_modified : devices []: leafref : /ncs:devices/ncs:device/ncs:name 
l3vpn_I_vpn_I_l3vpn_I_modified : services []: instance-identifier 
l3vpn_I_vpn_I_l3vpn_I_modified : lsa-services []: instance-identifier 
class "directly-modified" as  l3vpn_I_vpn_I_l3vpn_I_directly_modified <<container>> 
l3vpn_I_vpn_I_l3vpn *-- "1" l3vpn_I_vpn_I_l3vpn_I_directly_modified 
l3vpn_I_vpn_I_l3vpn_I_directly_modified : callpoint:ncs()
l3vpn_I_vpn_I_l3vpn_I_directly_modified : devices []: leafref : /ncs:devices/ncs:device/ncs:name 
l3vpn_I_vpn_I_l3vpn_I_directly_modified : services []: instance-identifier 
l3vpn_I_vpn_I_l3vpn_I_directly_modified : lsa-services []: instance-identifier 
l3vpn_I_vpn_I_l3vpn : get-modifications( in: outformat in: reverse in: service_depth in: choice_lsa_grouping)
l3vpn_I_vpn_I_l3vpn : un-deploy( in: ignore_refcount in: dry_run in: ncs_commit_params out: ncs_commit_result)
l3vpn_I_vpn_I_l3vpn : used-by-customer-service []: leafref : /ncs:services/ncs:customer-service/ncs:object-id  {Config : false}
class "commit-queue" as  l3vpn_I_vpn_I_l3vpn_I_commit_queue <<container>> 
l3vpn_I_vpn_I_l3vpn *-- "1" l3vpn_I_vpn_I_l3vpn_I_commit_queue 
l3vpn_I_vpn_I_l3vpn_I_commit_queue : cdboper()
l3vpn_I_vpn_I_l3vpn_I_commit_queue : clear()
class "queue-item" as l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item << (L, #FF7700) list>> 
l3vpn_I_vpn_I_l3vpn_I_commit_queue *-- "0..N" l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item 
l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item : +id : uint64  {key} 
l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item : status : enumeration : {waiting,executing,blocking,...}  
l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item : cleared-by-admin : empty  
class "failed-device" as l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item_I_failed_device << (L, #FF7700) list>> 
l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item *-- "0..N" l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item_I_failed_device 
l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item_I_failed_device : +name : leafref : /ncs:devices/ncs:device/ncs:name  {key} 
l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item_I_failed_device : time : yang:date-and-time  
l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item_I_failed_device : config-data : string  
l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item_I_failed_device : error : string  
l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item : admin-clear()
l3vpn_I_vpn_I_l3vpn_I_commit_queue_I_queue_item : delete()
class "private" as  l3vpn_I_vpn_I_l3vpn_I_private <<container>> 
l3vpn_I_vpn_I_l3vpn *-- "1" l3vpn_I_vpn_I_l3vpn_I_private 
l3vpn_I_vpn_I_l3vpn_I_private : diff-set : binary  
l3vpn_I_vpn_I_l3vpn_I_private : forward-diff-set : binary  
l3vpn_I_vpn_I_l3vpn_I_private : device-list []: string 
l3vpn_I_vpn_I_l3vpn_I_private : ned-id-list []: string 
l3vpn_I_vpn_I_l3vpn_I_private : service-list []: instance-identifier 
l3vpn_I_vpn_I_l3vpn_I_private : lsa-service-list []: yang:xpath1.0 
l3vpn_I_vpn_I_l3vpn_I_private : synthesizer-kicker-list []: instance-identifier 
class "property-list" as  l3vpn_I_vpn_I_l3vpn_I_private_I_property_list <<container>> 
l3vpn_I_vpn_I_l3vpn_I_private *-- "1" l3vpn_I_vpn_I_l3vpn_I_private_I_property_list 
class "property" as l3vpn_I_vpn_I_l3vpn_I_private_I_property_list_I_property << (L, #FF7700) list>> 
l3vpn_I_vpn_I_l3vpn_I_private_I_property_list *-- "0..N" l3vpn_I_vpn_I_l3vpn_I_private_I_property_list_I_property 
l3vpn_I_vpn_I_l3vpn_I_private_I_property_list_I_property : +name : string  {key} 
l3vpn_I_vpn_I_l3vpn_I_private_I_property_list_I_property : value : string  
l3vpn_I_vpn_I_l3vpn_I_private : re-deploy-counter : int32   = 0 
l3vpn_I_vpn_I_l3vpn_I_private : latest-commit-params : binary  
l3vpn_I_vpn_I_l3vpn_I_private : latest-u-info : binary  
l3vpn_I_vpn_I_l3vpn : plan-location : instance-identifier   {Config : false}
class "log" as  l3vpn_I_vpn_I_l3vpn_I_log <<container>> 
l3vpn_I_vpn_I_l3vpn *-- "1" l3vpn_I_vpn_I_l3vpn_I_log 
l3vpn_I_vpn_I_l3vpn_I_log : cdboper()
l3vpn_I_vpn_I_l3vpn_I_log : purge( in: filter_input out: purged_log_entries)
class "log-entry" as l3vpn_I_vpn_I_l3vpn_I_log_I_log_entry << (L, #FF7700) list>> 
l3vpn_I_vpn_I_l3vpn_I_log *-- "0..N" l3vpn_I_vpn_I_l3vpn_I_log_I_log_entry 
l3vpn_I_vpn_I_l3vpn_I_log_I_log_entry : +when : yang:date-and-time  {key} 
l3vpn_I_vpn_I_l3vpn_I_log_I_log_entry : type : log-entry-t   {mandatory}
l3vpn_I_vpn_I_l3vpn_I_log_I_log_entry : level : log-entry-level-t   {mandatory}
l3vpn_I_vpn_I_l3vpn_I_log_I_log_entry : message : string  
l3vpn_I_vpn_I_l3vpn : as-number : uint32   {mandatory}
class "endpoint" as l3vpn_I_vpn_I_l3vpn_I_endpoint << (L, #FF7700) list>> 
l3vpn_I_vpn_I_l3vpn *-- "0..N" l3vpn_I_vpn_I_l3vpn_I_endpoint 
l3vpn_I_vpn_I_l3vpn_I_endpoint : +id : string  {key} 
l3vpn_I_vpn_I_l3vpn_I_endpoint : ce-device : leafref : /ncs:devices/ncs:device/ncs:name   {mandatory}
l3vpn_I_vpn_I_l3vpn_I_endpoint : ce-interface : string   {mandatory}
l3vpn_I_vpn_I_l3vpn_I_endpoint : ip-network : inet:ip-prefix   {mandatory}
l3vpn_I_vpn_I_l3vpn_I_endpoint : bandwidth : uint32   {mandatory}
class "qos" as  l3vpn_I_vpn_I_l3vpn_I_qos <<container>> 
l3vpn_I_vpn_I_l3vpn *-- "1" l3vpn_I_vpn_I_l3vpn_I_qos 
l3vpn_I_vpn_I_l3vpn_I_qos : qos-policy : leafref : /l3vpn:qos/qos-policy/name  
class "custom-qos-match" as l3vpn_I_vpn_I_l3vpn_I_qos_I_custom_qos_match << (L, #FF7700) list>> 
l3vpn_I_vpn_I_l3vpn_I_qos *-- "0..N" l3vpn_I_vpn_I_l3vpn_I_qos_I_custom_qos_match 
l3vpn_I_vpn_I_l3vpn_I_qos_I_custom_qos_match : +name : string  {key} 
l3vpn_I_vpn_I_l3vpn_I_qos_I_custom_qos_match : qos-class : leafref : /l3vpn:qos/qos-class/name   {mandatory}
l3vpn_I_vpn_I_l3vpn_I_qos_I_custom_qos_match : source-ip : qos-match-type  
l3vpn_I_vpn_I_l3vpn_I_qos_I_custom_qos_match : destination-ip : qos-match-type  
l3vpn_I_vpn_I_l3vpn_I_qos_I_custom_qos_match : port-start : inet:port-number  
l3vpn_I_vpn_I_l3vpn_I_qos_I_custom_qos_match : port-end : inet:port-number  
l3vpn_I_vpn_I_l3vpn_I_qos_I_custom_qos_match : protocol : protocol-type  
class "/ncs:devices/ncs:device" as tailf_ncs_devices_I_devices_I_device <<leafref>> 
class "/qos/qos-class" as l3vpn_I_qos_I_qos_class <<leafref>> 
class "/ncs:devices/ncs:device" as tailf_ncs_devices_I_devices_I_device <<leafref>> 
l3vpn_I_topology_I_role-->"ncs:name"tailf_ncs_devices_I_devices_I_device: device
l3vpn_I_qos_I_qos_policy_I_class-->"name"l3vpn_I_qos_I_qos_class: qos-class
l3vpn_I_vpn_I_l3vpn_I_endpoint-->"ncs:name"tailf_ncs_devices_I_devices_I_device: ce-device
l3vpn_I_vpn_I_l3vpn_I_qos-->"name"l3vpn_I_qos_I_qos_policy: qos-policy
l3vpn_I_vpn_I_l3vpn_I_qos_I_custom_qos_match-->"name"l3vpn_I_qos_I_qos_class: qos-class
@enduml

```

## Pre-requisites

ncs-uml supports both trains of **python** `2.7+ and 3.1+`, the OS should not matter.

- pyang is used to translate the data.

## Installation and Downloads

The best way to get ncs-uml is with setuptools or pip. If you already have setuptools, you can install as usual:

`python -m pip install ncs-uml`

Otherwise download it from PyPi, extract it and run the `setup.py` script

`python setup.py install`

If you're Interested in the source, you can always pull from the github repo:

- From github `git clone https://github.com/kirankotari/ncs-uml.git`

## FAQ

- **Question:** Can we create uml diagram for the yang sub-module?  
 **Answer:** No, currently we are allowing modules only, we are going to add sub-modules to the module before generating uml diagram

- **Question:** Can I create uml diagram for 2 files at at time?  
 **Answer:** No, currently we are allowing one file at a time.

## Bug Tracker and Support

- Please report any suggestions, bug reports, or annoyances with pingping through the [Github bug tracker](https://github.com/kirankotari/ncs-uml/issues).


## License and Copyright

- ncs-uml is licensed [Apache 2.0](https://opensource.org/license/apache-2-0/) *2023*

   [![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-yellow)](https://opensource.org/license/apache-2-0/)

## Author and Thanks

ncs-uml was developed by [Kiran Kumar Kotari](https://github.com/kirankotari)