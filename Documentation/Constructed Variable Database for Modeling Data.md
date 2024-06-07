
# Data Constructs Documentation

## 1. sc_poverty
- **ACS**: Created using the POVPIP variable.
  - Categories:
    - POVPIP <= 99: 1 (Below poverty level)
    - POVPIP >= 100 & POVPIP <= 199: 2 (100%-199% of poverty level)
    - POVPIP >= 200 & POVPIP <= 299: 3 (200%-299% of poverty level)
    - POVPIP >= 300: 4 (300% and above of poverty level)
- **CHIS**: Directly copied from POVLL.
  - Original CHIS categories:
    - 1: 0-99% FPL
    - 2: 100-199% FPL
    - 3: 200-299% FPL
    - 4: 300% FPL AND ABOVE

## 2. sc_marit
- **ACS**: Copied from MAR variable.
- **CHIS**: Created using the AH43 variable.
  - Categories:
    - AH43 == 1: 1 (Married)
    - AH43 == 3: 2 (Widowed)
    - AH43 == 4: 3 (Divorced)
    - AH43 == 5: 4 (Separated)
    - AH43 == 2 | AH43 == 6: 5 (Never married/Other)
  - Original CHIS categories:
    - 1: Married
    - 2: Widowed
    - 3: Divorced
    - 4: Separated
    - 5: Never married
    - 6: Other

## 3. sc_emp
- **ACS**: Created using the ESR variable.
  - Categories:
    - ESR == 1 | ESR == 4: 1 (Employed)
    - ESR == 2 | ESR == 5: 2 (Unemployed)
    - ESR == 3 | ESR == 6: 3 (Not in labor force)
- **CHIS**: Created using the WRKST variable.
  - Categories:
    - WRKST == 1 | WRKST == 2: 1 (Employed)
    - WRKST == 3: 2 (Unemployed)
    - WRKST == 4 | WRKST == 5: 3 (Not in labor force)
  - Original CHIS categories:
    - 1: Employed
    - 2: Unemployed
    - 3: Not in labor force

## 4. sc_housing
- **ACS**: Created using the TEN variable.
  - Categories:
    - TEN == 1 | TEN == 2: 1 (Owner-occupied)
    - TEN == 3 | TEN == 4: 2 (Renter-occupied)
- **CHIS**: Directly copied from SRTENR.
  - Original CHIS categories:
    - 1: Owner-occupied
    - 2: Renter-occupied

## 5. sc_race_ethi
- **ACS**: Created using the HISP and RAC1P variables.
  - Categories:
    - HISP != 1: 1 (Not Hispanic)
    - RAC1P == 1: 2 (White alone)
    - RAC1P == 2: 3 (Black or African American alone)
    - RAC1P == 3 | RAC1P == 4 | RAC1P == 5: 4 (American Indian and Alaska Native alone)
    - RAC1P == 6: 5 (Asian alone)
    - RAC1P == 7: 6 (Native Hawaiian and Other Pacific Islander alone)
    - RAC1P == 8 | RAC1P == 9: 7 (Some other race alone, or two or more races)
- **CHIS**: Directly copied from OMBSRREO.
  - Original CHIS categories:
    - 1: Hispanic
    - 2: White, non-Hispanic
    - 3: African American only, not Hispanic
    - 4: American Indian/Alaska Native only, NH
    - 5: Asian only, NH
    - 6: Native Hawaiian/Pacific Islander, NH
    - 7: Two or more races, NH

## 6. sc_cit
- **ACS**: Created using the CIT variable.
  - Categories:
    - CIT == 1 | CIT == 2 | CIT == 3: 1 (Native)
    - CIT == 4: 2 (Naturalized citizen)
    - CIT == 5: 3 (Not a citizen)
- **CHIS**: Directly copied from CITIZEN2.
  - Original CHIS categories:
    - 1: Native
    - 2: Naturalized citizen
    - 3: Not a citizen

## 7. sc_edu
- **ACS**: Created using the SCHL variable.
  - Categories:
    - SCHL >= 1 & SCHL <= 15: 1 (Less than high school)
    - SCHL >= 16 & SCHL <= 17: 2 (High school graduate)
    - SCHL >= 18 & SCHL <= 20: 3 (Some college or associate's degree)
    - SCHL >= 21: 4 (Bachelor's degree or higher)
- **CHIS**: Directly copied from SREDUC.
  - Original CHIS categories:
    - 1: Less than high school
    - 2: High school graduate
    - 3: Some college
    - 4: College degree or higher

## 8. sc_ins
- **ACS**: Directly copied from HICOV.
- **CHIS**: Directly copied from INS.
  - Original CHIS categories:
    - 1: Insured
    - 2: Uninsured

## 9. sc_age_cat
- **ACS**: Created using the AGEP variable.
  - Categories:
    - AGEP < 18: 0 (Under 18)
    - AGEP >= 18 & AGEP < 25: 1 (18-24)
    - AGEP >= 25 & AGEP < 35: 2 (25-34)
    - AGEP >= 35 & AGEP < 45: 3 (35-44)
    - AGEP >= 45 & AGEP < 55: 4 (45-54)
    - AGEP >= 55 & AGEP <= 64: 5 (55-64)
    - AGEP >= 65: 6 (65 and over)
- **CHIS**: Created using the SRAGE variable.
  - Categories:
    - SRAGE < 18: 0 (Under 18)
    - SRAGE >= 18 & SRAGE < 25: 1 (18-24)
    - SRAGE >= 25 & SRAGE < 35: 2 (25-34)
    - SRAGE >= 35 & SRAGE < 45: 3 (35-44)
    - SRAGE >= 45 & SRAGE < 55: 4 (45-54)
    - SRAGE >= 55 & SRAGE <= 64: 5 (55-64)
    - SRAGE >= 65: 6 (65 and over)
  - Original CHIS categories:
    - 1: Under 18
    - 2: 18-24
    - 3: 25-34
    - 4: 35-44
    - 5: 45-54
    - 6: 55-64
    - 7: 65 and over

## 10. sc_hisp
- **ACS**: Created using the HISP variable.
  - Categories:
    - HISP == 1: 2 (Hispanic)
    - HISP != 1: 1 (Non-Hispanic)
- **CHIS**: Created using the SRH variable.
  - Categories:
    - SRH == 1: 1 (Hispanic)
    - SRH != 1: 2 (Non-Hispanic)
  - Original CHIS categories:
    - 1: Hispanic
    - 2: Non-Hispanic

## 11. sc_sex
- **ACS**: Created using the SEX variable.
  - Categories:
    - SEX == 1: 1 (Male)
    - SEX == 2: 2 (Female)
- **CHIS**: Created using the SRSEX variable.
  - Categories:
    - SRSEX == 1: 1 (Male)
    - SRSEX == 2: 2 (Female)
  - Original CHIS categories:
    - 1: Male
    - 2: Female
