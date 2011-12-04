from math import floor, log

# Python port of:
# https://www.microsoft.com/security/pc-security/assets/scripts/passwdcheck.js
#
# Main Page:
# https://www.microsoft.com/security/pc-security/password-checker.aspx
###############################################################################

__version__ = "1.0"
__author__ = "nomuus"
__copyright__ = "Microsoft"
__email__ = "mu*nre*txemusu*da"[::-1].replace('*', '') + "!@#$%^&*()"[1] + "nomuus" + "+..com"[2:]
__company__ = "www.nomuus.com"
__description__ = "Python Port of Microsoft Password Checker"

###############################################################################

alpha = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
punct = "~`!@#$%^&*()-_+="
digit = "1234567890"
total_chars = 0x7f - 0x20
alpha_chars = len(alpha)
upper_chars = len(upper)
digit_chars = len(digit)
upper_punct = len(punct)
other_chars = total_chars - (alpha_chars + upper_chars + upper_punct + digit_chars)
strength_labels = ["None", "Weak", "Medium", "Strong", "Best"]

###############################################################################

def calculate_bits(password):
	len_pwd = len(password)
	if len_pwd < 1:
		return 0
	
	b_alpha = False
	b_upper = False
	b_digit = False
	b_punct = False
	b_other = False
	charset = 0
	
	for c in password:
		if alpha.find(c) != -1:
			b_alpha = True
		elif upper.find(c) != -1:
			b_upper = True
		elif digit.find(c) != -1:
			b_digit = True
		elif punct.find(c) != -1:
			b_punct = True
		else:
			b_other = True
	
	if b_alpha:
		charset += alpha_chars
	if b_upper:
		charset += upper_chars
	if b_digit:
		charset += digit_chars
	if b_punct:
		charset += upper_punct
	if b_other:
		charset += other_chars

	bits = log(charset) * (len_pwd / log(2))
	return floor(bits)
	
###############################################################################
	
def eval_strength(password):
	bits = calculate_bits(password)
	if bits >= 128:
		display_strength(4)
	elif bits < 128 and bits >= 64:
		display_strength(3)
	elif bits < 64 and bits >= 56:
		display_strength(2)
	elif bits < 56:
		display_strength(1)
	else:
		display_strength(0)

###############################################################################

def display_strength(index):
	print strength_labels[index]
	
###############################################################################
###############################################################################

if __name__ == "__main__":
	x = raw_input("Enter a password: ")
	eval_strength(x)
