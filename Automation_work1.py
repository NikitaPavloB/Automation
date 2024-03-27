import subprocess
import string

def check_output_mode(text, mode='line'):
    if mode == 'line':
        res = subprocess.run(text, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
        output = res.stdout.split("\n")
    elif mode == 'word':
        res = subprocess.run(text, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
        output = res.stdout.split()
        output = [''.join(filter(lambda x: x not in string.punctuation, word)) for word in output]
    else:
        raise ValueError("Unsupported mode. Please choose either 'line' or 'word'.")
    
    if not res.returncode:
        return output
    else:
        return []

output_lines = check_output_mode("cat /etc/os-release", mode='line')
output_words = check_output_mode("cat /etc/os-release", mode='word')

print("Words from the output:")
print(output_words)  # Вывод списка слов из вывода

if 'VERSION="22.04.1 LTS (Jammy Jellyfish)"' in output_lines and 'VERSION_CODENAME=jammy' in output_lines:
    print("SUCCESS")

if 'VERSION' in output_words:
    print("The word 'VERSION' is present in the output.")
else:
    print("The word 'VERSION' is not present in the output.")
