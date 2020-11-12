
import os
out = os.path.abspath(os.path.join('path', 'test.csv'))

print(out)

LA5_MAPPING = {
    '31':'C010',
    '32A':'C010',
    '32ASB':'C011',
    '32I':'C012',
    '32N':'C013',
    '32EP':'C014',
    '32EPR':'C014',
    '32CAL':'C015',
    '6SF05':'C016',
    '42':'C017',
    '32L':'C018',
    'DIRECTLY':'C018',
    'AGENCY':'C018',
    '31HP':'C019',
    '32IP':'C019',
    '6SF03':'C020',
    '82':'D010',
    '44':'D020',
    '83':'D020',
    '32C':'D030',
    '36':'D040',
    '01':'E001',
    '08P':'E002',
    '32T':'E010',
    '13H':'E011',
    '13A':'E030',
    '13B':'E040',
    '13C':'E050',
    '13M':'E060',
    '13X':'E061',
    '11':'F001',
    '08':'F002',
    '12':'F020',
    '13G':'S002',
    '13Y':'S010',
    '36D':'SO30',
    '36DREP':'S031',
    '36DELE':'S032',
    '36DGAS':'S033',
    '36DVOIDS':'S034',
    '36DUMBR':'S035',
    '36G':'S033',
    '36V':'S034'

}

ACCOUNT_TEAM_MAPPING = {
    '210200':'36DREP',
    '200115':'36DREP',
    '210600':'36DVOIDS',
    '250000':'36DUMBR',
    '230100':'36DGAS',
    '250250':'36DUMBR',
    '230':'36DREP', #need to go through the mapping between 230 and 240
    '280180':'36DUMBR',
    '280220':'36DREP',
    '200106':'36DELE',
    '200136':'36DREP',
    '200110':'36DUMBR',
    '200111':'36DUMBR',
    '200114':'36DUMBR',
    '200119':'36DREP',
    '200127':'36DGAS',
    '250270':'36DGAS', #need to correctly map the breakdown of compenent repairs
    '700440':'36DGAS',
}