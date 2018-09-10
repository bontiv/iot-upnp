asyncio and UPnP
================

IoT-UPnP use asyncio for events handling. You can specify the loop which
will handle events with the initLoop method of the announcer class.

.. highlight:: python

    loop = asyncio.get_event_loop()

    server = Annoncer(device)
    server.initLoop(loop)

    loop.run_forever()

  The announcer class will use the ``asyncio.get_event_loop()`` when no loop
  are specified.
