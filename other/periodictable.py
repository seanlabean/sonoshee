import sys
import pandas as pd

def get_element_data(index):
    # read in data from csv file
    df = pd.read_csv('elements.tsv', sep='\t')
    df.columns = ['Atomic Number', 'Atomic Symbol', 'Name', 'Name Origin', 'Group', 'Period', 'Block', 'Atomic Weight', 'Density', 'Melting Point', 'Boiling Point', 'Heat Capacity', 'Electronegativity', 'Abundance in Earth\'s Crust', 'Origin', 'Phase at r.t.']
    if type(index) == str:
        # if index is a string, get element data by atomic symbol
        df = df.set_index('Atomic Symbol')
        # find dataframe index of atomic symbol
        index = df.index.get_loc(index)
    else:
        # set index to atomic number
        df = df.set_index('Atomic Number')
        index -= 1
    # return dataframe
    return df.iloc[index]

def main():
    while True:
        # show periodic table and get user input
        print('''
        H                                                                   He  
        Li  Be                                          B   C   N   O   F   Ne
        Na  Mg                                          Al  Si  P   S   Cl  Ar
        K   Ca  Sc  Ti  V   Cr  Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr
        Rb  Sr  Y   Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd  In  Sn  Sb  Te  I   Xe
        Cs  Ba  La  Hf  Ta  W   Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi  Po  At  Rn
        Fr  Ra  Ac  Rf  Db  Sg  Bh  Hs  Mt  Ds  Rg  Cn  Nh  Fl  Mc  Lv  Ts  Og
                
                Ce  Pr  Nd  Pm  Sm  Eu  Gd  Tb  Dy  Ho  Er  Tm  Yb  Lu
                Th  Pa  U   Np  Pu  Am  Cm  Bk  Cf  Es  Fm  Md  No  Lr
                ''')
        print('Enter atomic symbol or number to examine, or QUIT to quit.')
        response = input('> ')
        if response in ['QUIT', 'quit', 'Quit', 'q', 'Q', 'exit', 'Exit', 'EXIT']:
            print('Goodbye!')
            sys.exit()
        try:
            # if user input is a number, get element data by atomic number
            atomic_number = int(response)
            element_data = get_element_data(atomic_number)
            print(element_data)
        except ValueError:
            try:
                # if user input is a string, get element data by atomic symbol
                atomic_symbol = response
                element_data = get_element_data(atomic_symbol)
                print(element_data)
            except:
                # if user input is not a number or string, print error message
                print('Invalid input. Please try again.')
        print('\n-----------------------\nPress ENTER to continue.')
        pause = input()



if '__main__' in __name__:
    print('\nThe Periodic Table of Elements')
    print('Written by Sean C. Lewis')
    print('-------------------------')
    main()
