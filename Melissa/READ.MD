## Overview
This will use a melissa account to validate the county for many address's all at once. 

To use this you will need to have a melissa key from Melissa.com. 
You will use the Key that is tied to credits. Feel free to put both account Keys into thge Key.txt file if you are unsure. 

Add address's to the address txt. 

Run Python - Discrpinces file will be output with timestamp. 
## Install
Add key from Melisa account into Key.txt
Add Address's into address txt. 
    Seperate all address's with a full line space

## Run 
CD into file root
python "Melissa_ Address_ Verify.py"

## ERRORS
401 - You have run out of tokens for the day. Try again later. 
Address not processing correctly. - Remove all  " and other symbols in the address line.
Address Process but County is not found - See if county is in Fips list. - Only CO, MO, and KS are currently in fips list. 
