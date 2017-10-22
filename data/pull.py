import genomelink
import os

# callback = 'http://localhost:5000/callback'
#
# os.environ['GENOMELINK_CLIENT_ID'] = '3nlzyb6l5sBEjOn8Roy4iNODY1C4wjOhRPOW4AuI'
# os.environ['GENOMELINK_CALLBACK_URL'] = callback
# os.environ['GENOMELINK_CLIENT_SECRET'] = '35Pmz00KUARQcziFOL4wPkph6vcVswOiUnDHQVAC8aZQugqTqoN8qF1JDU7GR6HU5lPHxrwklYH7IaCL6qDsBp2AcV4u7jLbeTbEZoD6mGBSsPNgKl26u6CktflobhGV'

import pandas as pd
with open('pheno.features', 'r') as f:
    features = [str.rstrip() for str in f.readlines()]
    print(features)
pheno = pd.read_csv('phenotypes - scores_pseudo_users.csv', usecols=features)

full_pheno = pheno.as_matrix()
print(full_pheno.shape)