#for AIDS adult, elderly
# need to add ORs, from literature values, will need to map 'diseases' in 'HIV' to diseases in OR_G, need to add all aids defining 
# illnesses to OR_G
# For now can give all of the aids defining illnesses a default OR value, say 10. 
# Note HIV with CD4 <200, or HIV+ and aids defining illess = AIDs. For now can put AIDs as a demographic (known)
# ###########

e2eAdult = {'AIDS' :'Candidiasis of bronchi, trachea, or lungs','Candidiasis esophageal',
'Coccidioidomycosis, disseminated or extrapulmonary',
'Cryptococcosis, extrapulmonary',
'Cryptosporidiosis, chronic intestinal for longer than 1 month',
'Cytomegalovirus disease (other than liver, spleen or lymph nodes)',
'Cytomegalovirus retinitis (with loss of vision)',
'Encephalopathy (HIV-related)',
'Herpes simplex: chronic ulcer(s) (for more than 1 month); or bronchitis, pneumonitis, or esophagitis',
'Histoplasmosis, disseminated or extrapulmonary',
'Isosporiasis, chronic intestinal (for more than 1 month)',
'Kaposis sarcoma',
'Lymphoma, Burkitts',
'Lymphoma, immunoblastic (or equivalent term)',
'Lymphoma, primary, of brain',
'Mycobacterium avium complex or Mycobacterium kansasii, disseminated or extrapulmonary',
'Mycobacterium, other species, disseminated or extrapulmonary',
'Mycobacterium tuberculosis, any site (extrapulmonary)',
'Pneumocystis jiroveci pneumonia',
'Progressive multifocal leukoencephalopathy',
'Salmonella septicemia (recurrent)',
'Toxoplasmosis of the brain',
'Tuberculosis, disseminated',
'Wasting syndrome due to HIV',
'Cervical cancer (invasive)',
'Pneumonia (recurrent)'}

#for AIDS infants, and children

e2eChild = {'AIDS' :'Candidiasis of bronchi, trachea, or lungs','Candidiasis esophageal',
'Coccidioidomycosis, disseminated or extrapulmonary',
'Cryptococcosis, extrapulmonary',
'Cryptosporidiosis, chronic intestinal for longer than 1 month',
'Cytomegalovirus disease (other than liver, spleen or lymph nodes)',
'Cytomegalovirus retinitis (with loss of vision)',
'Encephalopathy (HIV-related)',
'Herpes simplex: chronic ulcer(s) (for more than 1 month); or bronchitis, pneumonitis, or esophagitis',
'Histoplasmosis, disseminated or extrapulmonary',
'Isosporiasis, chronic intestinal (for more than 1 month)',
'Kaposis sarcoma',
'Lymphoma, Burkitts',
'Lymphoma, immunoblastic (or equivalent term)',
'Lymphoma, primary, of brain',
'Mycobacterium avium complex or Mycobacterium kansasii, disseminated or extrapulmonary',
'Mycobacterium, other species, disseminated or extrapulmonary',
'Mycobacterium tuberculosis, any site (extrapulmonary)',
'Pneumocystis jiroveci pneumonia',
'Progressive multifocal leukoencephalopathy',
'Salmonella septicemia (recurrent)',
'Toxoplasmosis of the brain',
'Tuberculosis, disseminated',
'Wasting syndrome due to HIV',
'Cervical cancer (invasive)',
'Pneumonia (recurrent)',
'Bacterial infections, multiple or recurrent',
'Lymphoid interstitial pneumonia'}