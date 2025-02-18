import pandas as pd
from datetime import datetime, timedelta, date
from create_excel import manage_excel_file
from emails_sendgrid import send_emails

current = datetime.now() - timedelta(days=30)

expenses_df = pd.read_csv(
    f"C:\\Users\\nochum.paltiel\\OneDrive - Anchor Home Health care\\Documents\\Ramp Expenses\\Ramp Expenses {current.month}-{current.year}.csv")

categories_df = pd.read_csv(
    "C:\\Users\\nochum.paltiel\\OneDrive - Anchor Home Health care\\Documents\\Ramp Expenses\\Category Dropdown.csv")
category_options = [option for option in categories_df['Category']]
expenses_df = expenses_df[
    ['Transaction Time', 'Amount', 'User', 'User Email', 'Merchant Name', 'Merchant Description', 'Card Last 4',
     'Accounting Category', 'Accounting Class']]

users = expenses_df[['User', 'User Email']].drop_duplicates().reset_index(drop=True)

user_list = {users['User'][i]: expenses_df[expenses_df['User Email'] == users['User Email'][i]] for i in
             range(len(users['User Email']))}

for user in user_list:
    if user == 'Yekusiel kaplan':
        file = f"C:\\Users\\nochum.paltiel\\OneDrive - Anchor Home Health care\\Documents\\Ramp Expenses\\Ramp Expenses - {user}.xlsx"
        manage_excel_file(file, f'{current.strftime('%b')}-{current.year}', user_list[user], user, category_options)

        user_email = user_list[user]['User Email'].iloc[0]
        body = (f'Hi {user.split(" ")[0]},\n'
                f'        \n'
                f'Please see attached file for this months Ramp expenses.\n'
                f'Fill in the Confirmed Category and Approved columns. Feel free to add notes where applicable.\n'
                f'        \n'
                f'Please replay to this email with the amended file at your earliest convenience.\n'
                f'    \n'
                f'Thanks,\n'
                f'Berry')
        send_emails(user_email, f'Ramp Expenses - {user} ({date.today().strftime('%b %Y')})', body, file)
        break
