# OpenDNS Dashboard Browser
A client library for accessing resources provided by OpenDNS's Dashboard website.

This project's maintainers are not affiliated or employed by OpenDNS or its parent organization Cisco Systems, Inc.

> **IMPORTANT:**
>
> Please consider this project as an "alpha" release quality. Breaking changes may not always be documented or logged.

## Purpose
Enables an application to pull down reports from OpenDNS's Dashboard Statistics pages. With this library, an application can download Domain, Total Requests, Unique IP, Type Requests, and Unique Domain reports.

> **NOTE:**
>
> This library has been designed to be respectful of the provider's tolerance of these types of tools. When implementing this library in your projects, please remember you must continue to follow the provider's rules and agreements.


## Dependencies
Every effort is made to keep this library small and light. However some extra libraries are required to use the library as is.
* requests - https://requests.readthedocs.io/en/latest/
