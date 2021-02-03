# ticker

This is a thing to manage shopping lists that I run on an old Raspberry Pi taped to the back of an Epson TM-T88 type
thermal printer. With a few electronics bits the Pi is powered off of the TM-T88 (buck converter to reduce the printer's
24vdc to 5vdc) so it's sort of a self-contained appliance-esque object that sits on the counter. In fact if you have
the original rear cable cover for the TM-T88 you can use it to cover the Pi so it all looks rather professional.

An sqlite database is used to keep track of multiple lists which contain items. Items can be added and removed. Lists
can be added, removed, cleared (of all items), or printed, in which case they are sent to the TM-T88 to produce a nice
compact printed checklist in under a second.

Additional endpoints will shortly be added to allow you to send arbitrary strings or ESC/POS commands to be sent to a
separate serial printer, over either HTTP or MQTT. This is to replace a *separate* SBC taped to a TM-T88 that I use to
print a running log of burglar alarm, video surveillance, and home automation events, because UL says that commercial
burglar alarms should print a paper event log and I found that amusing. When you have a bad habit where you keep buying
high-speed thermal printers, you have to find things for them to do... call it a collection.