

def parse_cerberus_error_messages(validators):
    error_message = set()

    if type(validators) is not list:
        validators = [validators]

    for validator in validators:
        for (key, value) in validator.errors.items():
            for subvalue in value:
                try:
                    if type(subvalue) == dict:
                        for (subvalue_key, subvalue_value) in subvalue.items():
                            error_message.add(
                                '%s: %s' % (str(key) + '.' + str(subvalue_key), ', '.join(subvalue_value)))
                    else:
                        error_message.add('%s: %s' % (key, subvalue))
                except:
                    error_message.add('%s: %s' % (key, str(subvalue)))

    return list(error_message)

