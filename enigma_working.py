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

# def rotor(ID, input_char, r1_window = 'A', r1_ring_key = 0):
#     rotor_mapping = rotor_mappings[ID]
#     # rotor_notch = 'Q'
#     # rotor_current_mapping = [' ' for i in range(26)]
#     # coded_char = rotor_mapping[(char_to_int(input_char) - r1_ring_key + char_to_int(r1_window)) % 26]
#     coded_char = rotor_mapping[(char_to_int(input_char) - r1_ring_key) % 26]
#     return coded_char

# def rotor_inv(ID, input_char, window = 'A', ring_key = 0):
#     char_index = rotor_mappings[ID].index(input_char)
#     inverse_coded_char = int_to_char((char_index - ring_key + char_to_int(window)) % 26)
#     return inverse_coded_char

# def reflector(ID, char):
#     reflector_mappings[ID][char]

def encrypt_enigma(text, rotor_seq, rotor_ring, rotor_windows, reflector_id, plugboard_settings):
    encrypted_str = ""
    for char in text:
        last_rotor_windows = rotor_windows[:]
        # for i in range(2, len(rotor_seq) + 1):
        #     if rotor_windows[-1 * (i - 1)] == int_to_char((char_to_int(rotor_notches[rotor_seq[-1 * (i - 1)]]) + 1) % 26):
        #         # print("Got the notch: ", rotor_notches[rotor_seq[-1 * (i - 1)]], "of ", len(rotor_seq) - i)
        #         rotor_windows[-1 * i] = int_to_char((char_to_int(rotor_windows[-1 * i]) + 1) % 26)

        # for i in range(2, len(rotor_seq) + 1):
        #     if (last_rotor_windows[-1 * (i - 1)] == rotor_notches[rotor_seq[-1 * (i - 1)]]) and (rotor_windows[-1 * (i - 1)] == int_to_char((char_to_int(rotor_notches[rotor_seq[-1 * (i - 1)]]) + 1) % 26)):
        #         rotor_windows[-1 * i] = int_to_char((char_to_int(rotor_windows[-1 * i]) + 1) % 26)

        rotor_windows[-1] = int_to_char((char_to_int(rotor_windows[-1]) + 1) % 26)
        for i in range(1, len(rotor_seq) + 1):
            if last_rotor_windows[-1 * i] == rotor_notches[rotor_seq[-1 * i]]:
                if i != 1:
                    if last_rotor_windows[-1 * i] == rotor_windows[-1 * i]:
                        rotor_windows[-1 * i] = int_to_char((char_to_int(rotor_windows[-1 * i]) + 1) % 26)
                if last_rotor_windows[-1 * (i + 1)] == rotor_windows[-1 * (i + 1)]:
                    rotor_windows[-1 * (i + 1)] = int_to_char((char_to_int(rotor_windows[-1 * (i + 1)]) + 1) % 26)

        print("Last window: ", last_rotor_windows)
        print("Rotor_window: ", rotor_windows)



        if char in plugboard_settings.keys():
            propagate_char = plugboard_settings[char]
        elif char in plugboard_settings.values():
            propagate_char = list(plugboard_settings.keys())[list(plugboard_settings.values()).index(char)]
        else:
            propagate_char = char

        # print("After plugboard: ", propagate_char)


        for i in range(1, len(rotor_seq) + 1):
            # print(propagate_char)
            propagate_char = rotor_mappings[rotor_seq[-1 * i]][(char_to_int(propagate_char) - rotor_ring[-1 * i] + char_to_int(rotor_windows[-1 * i])) % 26]
            propagate_char = int_to_char((char_to_int(propagate_char) + rotor_ring[-1 * i] - char_to_int(rotor_windows[-1 * i])) % 26)
            # print("to", propagate_char)

        # for i in range(1, len(rotor_seq) + 1):
        #     print(propagate_char)
        #     # propagate_char = rotor(rotor_seq[-1 * i], propagate_char, rotor_windows[-1 * i], rotor_ring[-1 * i])
        #     if i == 1:
        #         propagate_char = rotor_mappings[rotor_seq[-1 * i]][(char_to_int(propagate_char) - rotor_ring[-1 * i] + char_to_int(rotor_windows[-1 * i])) % 26]
        #     else:
        #         propagate_char = rotor_mappings[rotor_seq[-1 * i]][(char_to_int(propagate_char) - rotor_ring[-1 * i]) % 26]
        #     if i < len(rotor_seq):
        #         advance_number = char_to_int(rotor_windows[-1 * i - 1]) - char_to_int(rotor_windows[-1 * i])
        #     else:
        #         advance_number = -1 * char_to_int(rotor_windows[-1 * i])
        #     print("to", propagate_char)
        #     print("advance number: ", advance_number)
        #     propagate_char = int_to_char((char_to_int(propagate_char) + advance_number - rotor_ring[-1 * i]) % 26)

        # print(propagate_char)
        propagate_char = reflector_mappings[reflector_id][propagate_char]
        # print("to", propagate_char)



        for i in range(len(rotor_seq)):
            # print(propagate_char)
            propagate_char = int_to_char((char_to_int(propagate_char) + char_to_int(rotor_windows[i]) - rotor_ring[i]) % 26)
            char_index = rotor_mappings[rotor_seq[i]].index(propagate_char)
            propagate_char = int_to_char((char_index + rotor_ring[i] - char_to_int(rotor_windows[i])) % 26)
            # print("to", propagate_char)
        # for i in range(len(rotor_seq)):
        #     print(propagate_char)
        #     char_index = rotor_mappings[rotor_seq[i]].index(propagate_char)
        #     propagate_char = int_to_char((char_index + rotor_ring[i]) % 26)
        #     # if i == 0:
        #     #     reversal_number = 0
        #     if i < len(rotor_seq) - 1:
        #         reversal_number = char_to_int(rotor_windows[i]) - char_to_int(rotor_windows[i + 1])
        #     else:
        #         reversal_number = char_to_int(rotor_windows[i])
        #     print("to", propagate_char)
        #     print("reversal no: ", reversal_number)
        #     propagate_char = int_to_char((char_to_int(propagate_char) - reversal_number) % 26)

        if propagate_char in plugboard_settings.keys():
            propagate_char = plugboard_settings[propagate_char]
        elif propagate_char in plugboard_settings.values():
            propagate_char = list(plugboard_settings.keys())[list(plugboard_settings.values()).index(propagate_char)]

        # print("Final Char: ", propagate_char)
        encrypted_str += propagate_char

    return encrypted_str

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
    print(rotor_ring_key)
    reflector_id = 0

    input_string = "PAZPIAFPWFPBDVECAZZVZWVFTVBPSQRNPHJLYVKFJCEQHIQVXT"
    input_string2 = "T"

    encrypted_text = encrypt_enigma(input_string, rotor_sequence, rotor_ring_key, rotor_windows, reflector_id, plugboard_settings)

    print(encrypted_text)

    # rotor_1_output = rotor(rotor_id, input_text, rotor_1_window, rotor_1_ring)
    # print(rotor_1_output)

if __name__ == "__main__":
    main()