
cmd_list  = ['ls : for command list','help : for help','add order <price> <size> : adds an order',
             'print vars : prints trader class variables', 'inventory : shows open orders',
             'cancel all orders : cancels all orders and exits', 'exit : exits the trading program',
             "<Type gibberish> : won't break processing",'description : describes the program'
             ]



def command_processing():
    command= input('-- ')
    if command == '':
        return None
    
    elif command == 'ls' or command == ' ls' or command == 'list commands' or command == 'help' :
        for i in cmd_list:
            print(i)
        return None
    
    elif command == 'description':
        print('This program was a product of me, Aleksey.')
        print('With user defined parameters,\nthis program will market make any stable coin on coinbase pro.')
        
        return None
    
    
    else:
        cmd  = (command.split(' '))
        if cmd[0] == '':
            cmd.remove('')
            restruct_cmd = ''
            for word in cmd:
                restruct_cmd = restruct_cmd+ f'{word} '
                command = restruct_cmd
        else:
            pass
        if cmd[0] == 'cancel' or cmd[0] == 'add':
            confirm = input('<Y> Confirm <X> Decline: ')
            if confirm == 'Y' or confirm == 'y':
                return command
            else:
                return 'canceled command'
                pass
        else:
            return command
            pass

while True:    
    with open('CBT_CMDS.csv', 'r+') as file:
        command = command_processing()
        if command == None:
            pass
        else:
            file.truncate(0)
            file.write(command)
    pass


  
    
    
    
    







