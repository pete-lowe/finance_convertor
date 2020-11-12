import csv
import os
from glob import glob
from collections import Counter
from src.mapping import LA5_MAPPING, ACCOUNT_TEAM_MAPPING

filename = glob('*csv')[0]

def open_headerless_csv(csv_file):
    f = open(csv_file)
    reader = csv.reader(f)
    return f

def read_csv_return_reader_object(open_csv_file):
    reader = csv.reader(open_csv_file)
    return reader

def write_list_to_csv(filename, list_to_write):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(list_to_write)

# def la4_mapper(jobnum, la1code):
#     if la1code[0:2] == 'MX':
#         return 'MX'
#     elif jobnum[0:2] == 'AH':
#         return 'AG'
#     elif jobnum[0:4] == 'GNSC':
#         return 'GN'
#     elif jobnum[0:2] == 'LH':
#         return la1code[0:2]
#     elif jobnum[0:3] == 'PML' or jobnum[0:3] == 'PMO':
#         return 'PL'
#     elif jobnum[0:3] == 'MOB':
#         return la1code[0:2]
#     elif jobnum[0:4] =='SBHA':
#         return 'GN'
#     elif jobnum[0:4] == 'SHEL':
#         return 'SH'
#     elif jobnum[0:2] == 'SH':
#         return 'SU'
#     else:
#         return '**Error**'
    
def la5_mapper(jobnum, la1code):
    if jobnum[0:2] == 'AH':
        return 'C018'
    elif jobnum[0:4] == 'GNSSC':
        return 'C010'
    elif jobnum[0:2] == 'LH':
        return 'C010'
    elif jobnum[0:2] == 'MX':
        return 'C010'
    elif (jobnum[0:3] == 'PMO' or jobnum[0:3] == 'PML') and la1code[0:2] != 'MX':
        return 'C018'
    elif (jobnum[0:3] == 'PMO' or jobnum[0:3] == 'PML') and la1code[0:2] == 'MX':
        return 'CO10'
    elif jobnum[0:3] == 'MOB' and la1code[0:2] in ('MX', 'LH', 'GN', 'SHEL'):
        return 'C010'
    elif jobnum[0:3] == 'MOB' and la1code[0:2] in ('AG', 'PL', 'SU'):
        return 'C018'
    elif jobnum[0:4] == 'SBHA':
        return 'C010'
    elif jobnum[0:4] == 'GNSC':
        return 'C010'
    elif jobnum[0:4] == 'SHEL':
        return 'C010'
    elif jobnum[0:2] == 'SH' and la1code[0:2] != 'MX':
        return 'C018'
    elif jobnum[0:2] == 'SH' and la1code[0:2] == 'MX':
        return 'C010'
    else:
        return '**Error**'


def main():
    transaction_date = '31/10/2020' #input('Enter transaction date (DD/MM/YYYY): ')
    financial_period = '007/2020' #input('Enter financial period (PPP/YYYY): ')

    #open the la mapping csv file
    la_mapping_csv = open_headerless_csv(os.path.abspath(os.path.join('src', 'la_mapping.csv')))
    la_csv_reader = read_csv_return_reader_object(la_mapping_csv)
        
    uprn_la1_mapping = {}
    uprn_la2_mapping = {}
    uprn_la4_mapping = {}

    #map uprn to la1, la2 and la4
    for row in la_csv_reader:
        uprn_la1_mapping[row[2]] = row[0]
        uprn_la2_mapping[row[2]] = row[1]
        uprn_la4_mapping[row[2]] = row[3]

    #open the nominal code mapping csv file
    nominal_mapping_csv = open_headerless_csv(os.path.abspath(os.path.join('src', 'nommap.csv')))
    nominal_csv_reader = read_csv_return_reader_object(nominal_mapping_csv)
    
    sun4_to_sun6_nominal_mapping = {}

    #dictionary of old codes to new - need to confirm that mapping doc correct
    for row in nominal_csv_reader:
        sun4_to_sun6_nominal_mapping[row[0]] = row[1]

    #open job margin report from accuserv
    job_margin_csv = open_headerless_csv(filename)
    job_margin_csv_reader = read_csv_return_reader_object(job_margin_csv)
    
    #create new list of lists to populate - same length as job_margin_csv
    new_rows_to_write = [[] for i in range(sum(1 for row in job_margin_csv_reader))]

    job_margin_csv.seek(0) #go to beginning of file

    for i, row in enumerate(job_margin_csv_reader):
        if row[2] == '2131' and row[3] == '36V':#check if job is allocated to void team
            new_rows_to_write[i].append('210600')
        elif row[2] == '2131' and row[3] == '36G':#check if job is allocated to gas team
            new_rows_to_write[i].append('230100')
        elif row[2] == '2131' and row[3] == '36Z':#check if job is allocated to gas team
            new_rows_to_write[i].append('200136')
        else:
            new_rows_to_write[i].append(sun4_to_sun6_nominal_mapping[row[2]]) #nominal mapping
        new_rows_to_write[i].append(financial_period)
        new_rows_to_write[i].append(transaction_date)
        new_rows_to_write[i].append(row[9].strip().replace('£', ''))
        new_rows_to_write[i].append(f'{row[7]}_{row[15][0:25 - len(row[7])]}') #description
        try:
            new_rows_to_write[i].append(uprn_la1_mapping[row[10]])
        except KeyError:
            new_rows_to_write[i].append('**Error**')
        if row[4]: #input la2 if job margin has a component code
            new_rows_to_write[i].append(uprn_la2_mapping[row[10]])
        else: 
            new_rows_to_write[i].append('')
        new_rows_to_write[i].append(row[10]) #la3 = uprn
        try:
            new_rows_to_write[i].append(uprn_la4_mapping[row[10]])
        except KeyError:
            new_rows_to_write[i].append('**Error**')
        try:
            new_rows_to_write[i].append(la5_mapper(row[7],uprn_la1_mapping[row[10]]))
        except KeyError:
            new_rows_to_write[i].append('**Error**')
        


    for row in new_rows_to_write: #remove , to allow conversion to float
        row[3] = row[3].replace(',', '')
    
    total_repair_costs = 0

    for row in new_rows_to_write: #calculate the total cost of all jobs
        total_repair_costs += float(row[3])



    nominal_recharge = {}

    for row in new_rows_to_write: #calculate total cost per nominal and add to dictionary
        if row[0] not in nominal_recharge:
            nominal_recharge[row[0]] = float(row[3])
        else:
            nominal_recharge[row[0]] += float(row[3])


    recharge_rows = []
    for i, rows in enumerate(new_rows_to_write):
        recharge_rows.append(['220100', financial_period, transaction_date,
                                  float(new_rows_to_write[i][3]) * -1, new_rows_to_write[i][4],
                                  '', '', '', '', LA5_MAPPING[ACCOUNT_TEAM_MAPPING[new_rows_to_write[i][0]]]])


    # for account in nominal_recharge: #total credited to relevant LA5 (team)
    #     new_rows_to_write.append(['220100', financial_period, transaction_date,
    #                         round(nominal_recharge[account], 2) * -1,
    #                         f'DOMUS {financial_period}', '', '', '', '',
    #                         LA5_MAPPING[ACCOUNT_TEAM_MAPPING[account]]])

    for rows in recharge_rows:
        new_rows_to_write.append(rows)

    new_rows_to_write.insert(len(new_rows_to_write),
                     ['600530', financial_period, transaction_date, round(total_repair_costs, 2) * -1,
                     f'DOMUS {financial_period}'])

    new_rows_to_write.insert(len(new_rows_to_write),
                        ['600530', financial_period, transaction_date, round(total_repair_costs, 2),
                        f'DOMUS {financial_period}'])

    new_rows_to_write.insert(0, ['Account', 'Period', 'Transaction Date', 'Amount',
                            'Description', 'LA1', 'LA2', 'LA3', 'LA4', 'LA5'])
        


    

    write_list_to_csv('SUN6conversion.csv', new_rows_to_write)

if __name__ == "__main__":
    main()
