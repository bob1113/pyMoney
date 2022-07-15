class Record: 
    """Represent a record.""" 
    def __init__(self, category, description, amount): 
        """Initialize a record by calling Record('meal', 'breakfast', -50)."""
        self._category = category
        self._description = description
        self._amount = amount
    @property
    def category(self):
        """View self._category"""
        return self._category
    
    @property
    def description(self):
        """View self._description"""
        return self._description
    
    @property
    def amount(self):
        """View self._amount"""
        return self._amount
        
class Records: 
    """Maintain a list of all the 'Record's and the initial amount of money.""" 
    def __init__(self): 
        """Initialize the records by reading from 'records.txt' or prompting for initial amount of money."""
        def initialize_1st_time():
            """Initialize the records by user (when this program executes first time)"""
            try: # handle the non-int input for initial_money
                self._initial_money = int(input('How much money do you have? '))
            except ValueError:
                sys.stderr.write('Invalid value for money. Set to 0 by default.')
                self._initial_money = 0
            finally:
                self._records = []

        self._records = []
        self._initial_money = 0
        try: # file doesn't exist (OSError)
            with open('records.txt','r') as fh: 
                self._initial_money = fh.readline()
                assert self._initial_money != '', 'empty file'
                assert type(int(self._initial_money)) == int, 'conversion error'

                self._initial_money = int(self._initial_money)
                for line in fh.readlines():
                    self._records.append((line.split()[0], line.split()[1], int(line.split()[2])))
                print('Welcome back!')
        except (OSError, AssertionError):
            return initialize_1st_time()
        except (ValueError, IndexError):
            sys.stderr.write('Invalid format in records.txt. Deleting the contents\n')
            open('records.txt', 'w').close() # clear file "records"
            return initialize_1st_time()
        
    def add(self, rec, categories): 
        """Adding a record to self._records with the format like meal breakfast -50"""
        try: # handle the format error like 'lunch-70'
            assert len(rec.split()) == 3, 'The format of a record should be like this: meal breakfast -50.\nFail to add a record.'
            try: # handle the value error like 'lunch -abc'
                rec = (rec.split()[0], rec.split()[1], int(rec.split()[2]))
                if categories.is_category_valid(rec[0]):
                    self._initial_money += rec[2]
                    self._records.append(rec)
                else:
                    sys.stderr.write('Invalid value for category.\nFail to add a record')
            except ValueError:
                sys.stderr.write('Invalid value for money.\nFail to add a record')
        except AssertionError as e:
            sys.stderr.write(str(e))    
            
    def view(self):
        """Print all the records and report the balance."""
        print("Here's your expense and income records:")
        print('Category\tDescription\tAmount')
        print('===========\t===========\t======')
        for r in self._records:
            print(f'{r[0]:<10}\t{r[1]:<10}\t{r[2]:<10}')
        print(f'Now you have {self._initial_money} dollars.')
        
    def delete(self, rec): 
        """Delete the specified record from self._records."""
        try: # handle format error of deletion 
            assert len(rec.split()) == 4, 'Invalid format. Fail to delete a record.'
            rec = [rec.split()[0], rec.split()[1], int(rec.split()[2]), int(rec.split()[3])]
            # handle the deletion of not existing data
            cnt = rec[3]
            count = 0 # counting for the element number in list 'records'
            found = False
            for r in self._records:
                if r[0] == rec[0] and r[1] == rec[1] and r[2] == rec[2]:
                    cnt -= 1
                    if cnt == 0:
                        found = True
                        self._initial_money -= r[2]
                        del self._records[count]
                count += 1
            if found == False:
                sys.stderr.write(f"There's no record with {rec[0]} {rec[1]} {rec[2]}. Fail to delete a record.")
        except AssertionError as e:
            sys.stderr.write(str(e))
            
    def find(self, target_categories): 
        """Print the records with certain category and report the balance."""
        print(f"""Here's your expense and income records under category "{category}":""")
        print('Category\tDescription\tAmount')
        print('===========\t===========\t======')
        temp_find = filter(lambda record: record[0] in target_categories, self._records)
        money = 0
        for r in temp_find:
            print(f'{r[0]:<10}\t{r[1]:<10}\t{r[2]:<10}')
            money += r[2]
        print(f'The total amount above is {money}.')
        
    def save(self): 
        """Write the initial money and all the records to 'records.txt'."""
        with open('records.txt','w') as fh:
            fh.write(f'{self._initial_money}\n')
            for r in self._records:
                fh.writelines(f'{r[0]} {r[1]} {r[2]}\n')

class Categories: 
    """Maintain the category list and provide some methods."""
    def __init__(self): 
        """Initialize self._categories as a nested list"""
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
    
    def view(self):
        """View all categories."""
        def view_categories(categories, level = 0): 
            if categories == None: 
                return
            if type(categories) in {list, tuple}: 
                for child in categories:
                    view_categories(child, level + 1) 
            else: 
                print(f'{" "*2*(level - 1)}- {categories}')
        view_categories(self._categories)
         
    def is_category_valid(self, category): 
        """Check whether a category is in self._categories"""
        def check(category, categories):
            for c in categories:
                if type(c) == list:
                    if check(category, c):
                        return True
                elif c == category:
                    return True
            return False        
        return check(category, self._categories)
                                                                          
    def find_subcategories(self, category):
        """Find the subcategories of certain category."""
        def find_subcategories_gen(category, categories, found=False): 
            def flat(lis):
                flatList = []
                # Iterate with outer list
                for element in lis:
                    if type(element) is list:
                        # Check if type is list than iterate through the sublist
                        for item in element:
                            flatList.append(item)
                    else:
                        flatList.append(element)
                return flatList
            if type(categories) == list: 
                for index, child in enumerate(categories): 
                    yield from find_subcategories_gen(category, child, False) 
                    if child == category and index + 1 < len(categories) and type(categories[index + 1]) == list: 
                        # When the target category is found, 
                        # recursively call this generator on the subcategories 
                        # with the flag set as True. 
                        yield from flat(categories[index + 1])
            else: 
                if categories == category or found == True: 
                    yield categories
        return [i for i in find_subcategories_gen(category, self._categories)]
    


import sys

categories = Categories() 
records = Records()

while True:
    cmd = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
    if cmd == 'add':
        rec = input('Add an expense or income record with category, description, and amount (separate by spaces):\n') 
        records.add(rec, categories)
    elif cmd == 'view': 
        records.view()
    elif cmd == 'delete':
        delete_record = input('Which record do you want to delete?\nThe input format is "cate desc amt cnt" (cnt means the serial number of the same name object counting from the front)\n')
        records.delete(delete_record)
    elif cmd == 'view categories':
        categories.view()
    elif cmd == 'find': 
        category = input('Which category do you want to find? ') 
        target_categories = categories.find_subcategories(category) 
        records.find(target_categories)
    elif cmd == 'exit': 
        records.save() 
        break
    else: 
        sys.stderr.write('Invalid command. Try again.\n')