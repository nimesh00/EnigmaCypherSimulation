rotor_mappings = ["EKMFLGDQVZNTOWYHXUSPAIBRCJ",
                  "AJDKSIRUXBLHWTMCQGZNPYFVOE",
                  "BDFHJLCPRTXVZNYEIWGAKMUSQO",
                  "ESOVPZJAYQUIRHXLNFTGKDCMWB",
                  "VZBRGITYUPSDNHLXAWMJQOFECK"]
rotor_notches = ['Q', 'E', 'V', 'J', 'Z']

reflector_mappings = [{"A":"Y","Y":"A","B":"R","R":"B","C":"U","U":"C","D":"H","H":"D","E":"Q","Q":"E","F":"S","S":"F","G":"L","L":"G","I":"P","P":"I","J":"X","X":"J","K":"N","N":"K","M":"O","O":"M","T":"Z","Z":"T","V":"W","W":"V"},
                      {"A":"F","F":"A","B":"V","V":"B","C":"P","P":"C","D":"J","J":"D","E":"I","I":"E","G":"O","O":"G","H":"Y","Y":"H","K":"R","R":"K","L":"Z","Z":"L","M":"X","X":"M","N":"W","W":"N","Q":"T","T":"Q","S":"U","U":"S"}]

def char_to_int(char):
    return ord(char) - 65

def int_to_char(num):
    return chr(num + 65)


# main enigma encryption/decryption function
def encrypt_enigma(text, rotor_seq, rotor_ring, rotor_windows, reflector_id, plugboard_settings):
    encrypted_str = ""
    for char in text:

        # rotor rotation
        rotor_windows[-1] = int_to_char((char_to_int(rotor_windows[-1]) + 1) % 26)
        for i in range(2, len(rotor_seq) + 1):
            if rotor_windows[-1 * (i - 1)] == int_to_char((char_to_int(rotor_notches[rotor_seq[-1 * (i - 1)]]) + 1) % 26):
                rotor_windows[-1 * i] = int_to_char((char_to_int(rotor_windows[-1 * i]) + 1) % 26)


        # input plugboard conversion
        if char in plugboard_settings.keys():
            propagate_char = plugboard_settings[char]
        elif char in plugboard_settings.values():
            propagate_char = list(plugboard_settings.keys())[list(plugboard_settings.values()).index(char)]
        else:
            propagate_char = char

        # first pass rotor encryption from right to left
        for i in range(1, len(rotor_seq) + 1):
            # print(propagate_char)
            propagate_char = rotor_mappings[rotor_seq[-1 * i]][(char_to_int(propagate_char) - rotor_ring[-1 * i] + char_to_int(rotor_windows[-1 * i])) % 26]
            propagate_char = int_to_char((char_to_int(propagate_char) + rotor_ring[-1 * i] - char_to_int(rotor_windows[-1 * i])) % 26)

        # reflector encryption
        propagate_char = reflector_mappings[reflector_id][propagate_char]

        # second pass rotor encryption from left to right
        for i in range(len(rotor_seq)):
            propagate_char = int_to_char((char_to_int(propagate_char) + char_to_int(rotor_windows[i]) - rotor_ring[i]) % 26)
            char_index = rotor_mappings[rotor_seq[i]].index(propagate_char)
            propagate_char = int_to_char((char_index + rotor_ring[i] - char_to_int(rotor_windows[i])) % 26)

        # output plugboard conversion
        if propagate_char in plugboard_settings.keys():
            propagate_char = plugboard_settings[propagate_char]
        elif propagate_char in plugboard_settings.values():
            propagate_char = list(plugboard_settings.keys())[list(plugboard_settings.values()).index(propagate_char)]

        # appending on the encrypted string
        encrypted_str += propagate_char

    return encrypted_str

def format_message(text):
    text = text.replace("XX", " ")
    text = text.replace("XNX", ",")
    text = text.replace("XPX", ".")
    text = text.replace("YQ ", "1 ")
    text = text.replace("YW ", "2 ")
    text = text.replace("YE ", "3 ")
    text = text.replace("YR ", "4 ")
    text = text.replace("YT ", "5 ")
    text = text.replace("YZ ", "6 ")
    text = text.replace("YU ", "7 ")
    text = text.replace("YI ", "8 ")
    text = text.replace("YO ", "9 ")
    text = text.replace("YP ", "0 ")
    return text


def main():
    rotor_sequence = [2, 0, 3]
    # rotor_sequence = [0, 1, 2]
    rotor_ring_key = [0, 0, 0]
    rotor_ring = ['E', 'W', 'Z']
    rotor_windows = ['Z', 'I', 'N']
    # AT BS DE FM IR KN LZ OW PV HQ
    plugboard_settings = {"A":"T", "B":"S", "D":"E", "F":"M", "I":"R", "K":"N", "L":"Z", "O":"W", "P":"V", "H":"Q"}

    for i in range(len(rotor_ring)):
        rotor_ring_key[i] = char_to_int(rotor_ring[i])
    reflector_id = 0

    # input_string = "PAZPIAFPWFPBDVECAZZVZWVFTVBPSQRNPHJLYVKFJCEQHIQVXT"
    # input_string2 = "THISXXISXXYQXXTESTXXFELEXXTOXXCHECKXXYOURXXCODEYPX"

    actual_data_file = open("encrypted.txt", "r")

    actual_string = actual_data_file.read()

    encrypted_text = encrypt_enigma(actual_string, rotor_sequence, rotor_ring_key, rotor_windows, reflector_id, plugboard_settings)

    # print(encrypted_text)

    final_string = format_message(encrypted_text)

    print("Formatted: message: \n", final_string)

    # rotor_1_output = rotor(rotor_id, input_text, rotor_1_window, rotor_1_ring)
    # print(rotor_1_output)

if __name__ == "__main__":
    main()