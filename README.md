Dataview Seattle 911 Notifier
============================

This script informs dataview of 911 activity in the Seattle area.

Usage
----

The following options must be passed when configuring an instance of the notifier:

* API_ENDPOINT
* API_TOKEN
* GEOFENCE

Example:

````python
processor = Seattle911IncidentProcessor('http://dataview.restricted.wl-net.net:8000/api/1/', '<API_KEY>', [[], [], [], []])
incidents = processor.process_incidents(processor.parse_incidents())
````

Geofencing
----
This script supports GeoJSON fencing to reduce the number of incidents reported to those of a particular area.


Address Monitoring
----
This script will support reporting of activities at specified addresses. This comes in handy if your building only activates fire alarms two floors above/below a fire.