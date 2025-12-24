*** Settings ***
Library    MQTTLibrary
Library    JSONLibrary
Library    Collections
# Since we use PYTHONPATH, we don't need paths here
Library    simulator.iot_device_simulator
*** Variables ***
${BROKER_HOST}    localhost
${BROKER_PORT}    1883
# Updated to your generic topic structure
${TOPIC}          iot/device/telemetry

*** Test Cases ***
Self Communication Test
    [Documentation]    Verify basic broker connectivity by publishing to ourselves.
    [Tags]             smoke    mqtt
    Connect            ${BROKER_HOST}    ${BROKER_PORT}
    Subscribe          test/connectivity    0
    #Publish from WITHIN the test to verify the loopback works
    Publish            test/connectivity    HELLO_BROKER
    Subscribe And Validate    test/connectivity    qos=0    payload=HELLO_BROKER    timeout=5
    Disconnect

Verify Device Logic With Custom Keyword
    [Documentation]    Uses the custom Python helper to fetch and validate the latest telemetry logic.
    [Tags]             regression    logic
    Connect            ${BROKER_HOST}    ${BROKER_PORT}
    Subscribe          ${TOPIC}    0
    
    #1. Wait for the simulator to send at least one heartbeat 
    Sleep              2s
    
    #2. Get the library instance to pass to our custom Python keyword 
    ${mqtt_lib}=       Get Library Instance    MQTTLibrary
    
    #3. Use the helper function from iot_device_simulator.py to get the latest message 
    ${payload}=        Get Latest Mqtt Message    ${mqtt_lib}    ${TOPIC}
    
    Should Not Be Equal    ${payload}    ${None}    msg=No telemetry received from the simulator! 
    
    #4. Parse the JSON and validate business logic 
    ${json_obj}=       Convert String To Json    ${payload}
    
    # Verify the ID matches our new generic SENSOR-01 
    Should Be Equal As Strings    ${json_obj['device_id']}    SENSOR-01
    
    #Validate the Air Quality Logic: CO2 < 1000 must be SAFE 
    IF    ${json_obj['co2_level']} < 1000
       Should Be Equal As Strings    ${json_obj['air_quality']}    SAFE 
    ELSE
      Should Be Equal As Strings    ${json_obj['air_quality']}    DANGER
    END
    
    Log    Validated Device: ${json_obj['device_id']} | CO2: ${json_obj['co2_level']} | Status: ${json_obj['air_quality']}
    Disconnect
