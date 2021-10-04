Introduction
=============

Laboratory management and information systems (LMS, LIMS) have developed in recent years to support and automate more
functions that are encountered in the laboratory on a regular basis. Commercial software facilitates experiment
planning, analysis and other lab related activities such as audit trail, storage and user management. However, they
always exclude device management and device control. A user is always required to to run the experiments step by step,
transfer data, and translate input. Device integration is time-consuming and requires the development of expensive
custom solutions.

The main reason for the lack of this functionality is more obvious than one might think. It all boils down to a lack of
standardization. Devices in a laboratory environment cannot be integrated easily into a control software making it near
impossible to conduct experiments that require many devices at once. Experiments that rely on inter-device communication
in real-time, experiments that need to be flexible, adjustable to new findings, require a framework for easy integration,
management, data access and workflow design.

This software is building on top of the SiLA 2 standard. SiLA 2 is a mission to establish international standards in
laboratory automation and to enable open connectivity and thus rapid integration capability.
Goals are interoperability, flexibility, resource optimization for laboratory instrument integration and software
services based on standardized communication protocols and content specifications. SiLA 2 is an open standard and is
maintained by the not-for-profit SiLA consortium.
The SiLA 2 standard is based on well established communication protocols (Http2, gRPC). SiLA 2 is based on an inherent
server-client architecture. Connection is established over a TCP/IP network. For more information visit the
`SiLA website <https://sila-standard.com/>`_ or check
out the `SiLA_Base <https://gitlab.com/SiLA2/sila_base>`_ repository on GitLab.

SiLA uses auto-discovery to broadcast services on the network. Accessing, managing and integrating these services
into workflows in the lab environment is not part of the SiLA standard. A software framework on the middleware level
is needed to connect and manage available lab devices. The proposed software provides the user with these additional
features.
