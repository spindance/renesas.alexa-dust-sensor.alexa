def qualitative_pcs_value(pcs_value):
    """Convert PCS value into qualitative description"""
    if pcs_value < 369:
        output = "Very good"
    elif pcs_value < 1088:
        output = "Good"
    elif pcs_value < 1700:
        output = "Standard"
    elif pcs_value < 4622:
        output = "Bad"
    elif pcs_value < 7696:
        output = "Very Bad"
    else:
        output = "Hazardous"
    return output

def handle_event():
    """Handle the trigger event"""
    pcs_value = IONode.get_input('in1')['event_data']['value']
    output = qualitative_pcs_value(pcs_value)
    IONode.set_output('out1', {"value": output})

handle_event()
