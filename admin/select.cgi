#!/usr/bin/ruby

$stdout.sync = true
$stderr.reopen $stdout

print "content-type: text/html\r\n\r\n"

require 'cgi'
require 'stringio'
require 'mysql2'

cgi = CGI.new("html5")

db = Mysql2::Client.new(:host=>'10.20.3.4',:username=> 'dbms_cg',:password => 'cg_27_levan', :database=> 'dbms_cg_dbA')

puts "<html>"
puts "<head>"
puts "<link rel='stylesheet'; href='styles.css'>"

if cgi['submitted'] == "true"
    #build selected columns
    column_list = []
    query = ""
    if cgi['p_id'] != ""
        query = "#{cgi['p_id']}"
        column_list.push("Passenger_ID")
    end
    if cgi['surv'] != ""
        if query == ""
            query = "#{cgi['surv']}"
        else
            query = query + ",#{cgi['surv']}"
        end
        column_list.push("Survive")
    end
    if cgi['honor'] != ""
        if query == ""
            query = "#{cgi['honor']}"
        else
            query = query + ",#{cgi['honor']}"
        end
        column_list.push("Honorific")
    end
    if cgi['fName'] != ""
        if query == ""
            query = "#{cgi['fName']}"
        else
            query = query + ",#{cgi['fName']}"
        end
        column_list.push("First Name")
    end
    if cgi['lName'] != ""
        if query == ""
            query = "#{cgi['lName']}"
        else
            query = query + ",#{cgi['lName']}"
        end
        column_list.push("Last Name")
    end
    if cgi['unName'] != ""
        if query == ""
            query = "#{cgi['unName']}"
        else
            query = query + ",#{cgi['unName']}"
        end
        column_list.push("Unmarried Name")
    end
    if cgi['gndr'] != ""
        if query == ""
            query = "#{cgi['gndr']}"
        else
            query = query + ",#{cgi['gndr']}"
        end
        column_list.push("Gender")
    end
    if cgi['a'] != ""
        if query == ""
            query = "#{cgi['a']}"
        else
            query = query + ",#{cgi['a']}"
        end
        column_list.push("Age")
    end
    if cgi['sos'] != ""
        if query == ""
            query = "#{cgi['sos']}"
        else
            query = query + ",#{cgi['sos']}"
        end
        column_list.push("Siblings/Spouses On Board")
    end
    if cgi['pok'] != ""
        if query == ""
            query = "#{cgi['pok']}"
        else
            query = query + ",#{cgi['pok']}"
        end
        column_list.push("Parents/Kids On Board")
    end
    if cgi['b_id'] != ""
        if query == ""
            query = "#{cgi['b_id']}"
        else
            query = query + ",#{cgi['b_id']}"
        end
        column_list.push("Boarding_ID")
    end
    if cgi['tNum'] != ""
        if query == ""
            query = "#{cgi['tNum']}"
        else
            query = query + ",#{cgi['tNum']}"
        end
        column_list.push("Ticket Number")
    end
    if cgi['fre'] != ""
        if query == ""
            query = "#{cgi['fre']}"
        else
            query = query + ",#{cgi['fre']}"
        end
        column_list.push("Fare")
    end
    if cgi['cab'] != ""
        if query == ""
            query = "#{cgi['cab']}"
        else
            query = query + ",#{cgi['cab']}"
        end
        column_list.push("Cabins")
    end
    if cgi['embfrm'] != ""
        if query == ""
            query = "#{cgi['embfrm']}"
        else
            query = query + ",#{cgi['embfrm']}"
        end
        column_list.push("Embarked From")
    end

    #build conditionals
    pass_query = ""
    if cgi['passenger_id'] != ""
        pass_query = "p.Passenger_ID #{cgi['passenger_id'].strip()} "
    end
    if cgi['survive'] != ""
        if pass_query == ""
            pass_query = "p.Survive #{cgi['survive'].strip()} "
        else
            pass_query = pass_query + "#{cgi['connector']} p.Survive #{cgi['survive'].strip()} "
        end
    end
    if cgi['honorific'] != ""
        if pass_query == ""
            pass_query = "p.Honorific #{cgi['honorific'].strip()} "
        else
            pass_query = pass_query + "#{cgi['connector']} p.Honorific #{cgi['honorific'].strip()} "
        end
    end
    if cgi['firstName'] != ""
        if pass_query == ""
            pass_query = "p.First_Name #{cgi['firstName'].strip()} "
        else
            pass_query = pass_query + "#{cgi['connector']} p.First_Name #{cgi['firstName'].strip()} "
        end
    end
    if cgi['lastName'] != ""
        if pass_query == ""
            pass_query = "p.Last_Name #{cgi['lastName'].strip()} "
        else
            pass_query = pass_query + "#{cgi['connector']} p.Last_Name #{cgi['lastName'].strip()} "
        end
    end
    if cgi['unmarriedName'] != ""
        if pass_query == ""
            pass_query = "p.Unmarried_Name #{cgi['unmarriedName'].strip()} "
        else
            pass_query = pass_query + "#{cgi['connector']} p.Unmarried_Name #{cgi['unmarriedName'].strip()} "
        end
    end
    if cgi['gender'] != ""
        if pass_query == ""
            pass_query = "p.Gender #{cgi['gender'].strip()} "
        else
            pass_query = pass_query + "#{cgi['connector']} p.Gender #{cgi['gender'].strip()} "
        end
    end
    if cgi['age'] != ""
        if pass_query == ""
            pass_query = "p.Age #{cgi['age'].strip()} "
        else
            pass_query = pass_query + "#{cgi['connector']} p.Age #{cgi['age'].strip()} "
        end
    end
    if cgi['boarding_id'] != ""
        if pass_query == ""
            pass_query = "p.Boarding_ID #{cgi['boarding_id'].strip()} "
        else
            pass_query = pass_query + "#{cgi['connector']} p.Boarding_ID #{cgi['boarding_id'].strip()} "
        end
    end
    if cgi['siblings'] != ""
        if pass_query == ""
           pass_query = "f.Siblings_Or_Spouses #{cgi['siblings'].strip()} "
        else
           pass_query = pass_query + "#{cgi['connector']} f.Siblings_Or_Spouses #{cgi['siblings'].strip()} "
        end
    end
    if cgi['parents'] != ""
        if pass_query == ""
           pass_query = "f.Parents_Or_Kids #{cgi['parents'].strip()} "
        else
           pass_query = pass_query + "#{cgi['connector']} f.Parents_Or_Kids #{cgi['parents'].strip()} "
        end
    end
    if cgi['ticketNumber'] != ""
        if pass_query== ""
            pass_query = "b.Ticket_Number #{cgi['ticketNumber'].strip()} "
        else
            pass_query = pass_query + "#{cgi['connector']} b.Ticket_Number #{cgi['ticketNumber'].strip()} "
        end
    end
    if cgi['class'] != ""
        if pass_query== ""
            pass_query = "b.Class #{cgi['class'].strip()} "
        else
            pass_query = pass_query + "#{cgi['connector']} b.Class #{cgi['class'].strip()} "
        end
    end
    if cgi['fare'] != ""
        if pass_query == ""
            pass_query = "b.Fare #{cgi['fare'].strip()} "
        else
            pass_query = pass_query + "#{cgi['connector']} b.Fare #{cgi['fare'].strip()} "
        end
    end
    if cgi['embarkedFrom'] != ""
        if pass_query == ""
            pass_query = "b.Embarked_From #{cgi['embarkedFrom'].strip()} "
        else
            pass_query = pass_query + "#{cgi['connector']} b.Embarked_From #{cgi['embarkedFrom'].strip()} "
        end
    end
    if cgi['cabins'] != ""
        cabin_query = ""
        if cgi['cabins'] == "IS NULL" || cgi['cabins'] == "IS NOT NULL"
            if pass_query == ""
                pass_query = "c.Cabin #{cgi['cabins']}"
            else
                pass_query = pass_query + "AND c.Cabins #{cgi['cabins']}"
            end
        else
            cabins = cgi['cabins'].strip().split(",")
            operator = cabins[0][0]
            # cabins are always an OR
            cabins.each() do |cabin|
                if cabin_query == ""
                    cabin_query =  "(c.Cabin #{cabin} "
                else
                    cabin_query = cabin_query + "OR c.Cabin #{operator} #{cabin} "
                end
            end
            if pass_query != ""
                pass_query = pass_query + "#{cgi['connector']} #{cabin_query}" 
            else
                pass_query = cabin_query + ")"
            end
        end
    end

    puts "<title>Query</title>"
    puts "</head>"
    puts "<header class='header'>"
    puts "<h1>Here is your queried table</h1>"
    puts "</header>"
    puts "<form method='post' action='admin.cgi' class='upload-form'>"
    puts "<button type='submit' class='upload-button'>Make Another Query</button>"
    puts "</form>"
    puts "<form method='post' action='ExportFile/queried.csv' class='exportCSV'>"
    puts "<button type='submit' class='upload-button'>Download a CSV</button>"

    everything = ['Passenger_ID', 'Survive', 'Honorific', 'First Name', 'Last Name', 'Unmarried Name', 'Gender', 'Age', 'Siblings/Spouses On Board', 'Parents/Kids On Board', 'Boarding_ID', 'Class','Ticket Number', 'Fare', 'Cabins', 'Embarked From']

    uploadLocation = "/NFSHome/cgartner/public_html/Final/admin/ExportFile/"

    file_path = uploadLocation + "queried.csv"
    
    puts "</form>"
    puts "<div class='scroll-container'>"
    puts "<div class='table-panel'>"
    puts "<table class='db'><tr>"
    puts "<caption>Titanic Passengers</caption>"
    puts "<thead>"
    begin
        File.open(file_path, "w") do |file|
            if query != ""
                columns = []
                column_list.each() do |col|
                    puts "<th>#{col}</th>"
                    columns.push(col)
                end
                file.puts(columns.join(","))
                puts "</thead>"
                puts "<tbody>"  
                currentTable = db.query("SELECT #{query} FROM  Passengers p LEFT JOIN Family_On_Board f ON p.Passenger_ID = f.Passenger_ID LEFT JOIN Boarding_Info b ON p.Boarding_ID = b.Boarding_ID LEFT JOIN Cabins c ON p.Passenger_ID = c.Passenger_ID WHERE #{pass_query} GROUP BY p.Passenger_ID;")
                currentTable.each() do |row|
                    puts "<tr>"
                    #when position is 2, d[1] is BOOL
                    position = 0
                    rowArray = []
                    row.each() do |d|
                        if d[1] == nil
                            puts "<td>NULL</td>"
                            rowArray.push("NULL")
                        elsif d[1] == 0 && column_list[position] == "Survive"
                            puts "<td>False</td>"
                            rowArray.push("False")
                        elsif d[1] == 1 && column_list[position] == "Survive"
                            puts "<td>True</td>"
                            rowArray.push("True")
                        else
                            puts "<td>#{d[1]}</td>" 
                            rowArray.push(d[1])
                        end 
                        position += 1
                    end
                    puts "</tr>"
                    file.puts(rowArray.join(","))
                end
            else
                everything.each() do |col|
                    puts "<th>#{col}</th>"
                end
                puts "</thead>"
                puts "<tbody>"
                #build a csv for export as we print the table
                file.puts(everything.join(","))
                currentTable = db.query("SELECT p.Passenger_ID, p.Survive, p.Honorific, p.First_Name, p.Last_Name,p.Unmarried_Name, p.Gender, p.Age, f.Siblings_Or_Spouses, f.Parents_Or_Kids, b.Boarding_ID, b.Class, b.Ticket_Number, b.Fare, GROUP_CONCAT(c.Cabin ORDER BY c.Cabin SEPARATOR ' ') AS Cabins, b.Embarked_From FROM  Passengers p LEFT JOIN Family_On_Board f ON p.Passenger_ID = f.Passenger_ID LEFT JOIN Boarding_Info b ON p.Boarding_ID = b.Boarding_ID LEFT JOIN Cabins c ON p.Passenger_ID = c.Passenger_ID WHERE #{pass_query} GROUP BY p.Passenger_ID;")
                currentTable.each() do |row|
                    puts "<tr>"
                    #when position is 2, d[1] is BOOL
                    position = 1
                    rowArray = []
                    row.each() do |d|
                        if d[1] == nil
                            puts "<td>NULL</td>"
                            rowArray.push("NULL")
                        elsif d[1] == 0 && position == 2
                            puts "<td>False</td>"
                            rowArray.push("False")
                        elsif d[1] == 1 && position == 2
                            puts "<td>True</td>"
                            rowArray.push("True")
                        else
                            puts "<td>#{d[1]}</td>" 
                            rowArray.push(d[1])
                        end 
                        position += 1
                    end
                    puts "</tr>"
                    file.puts(rowArray.join(","))
                end
            end
        end
        puts "</tbody>"
        puts "</table>"
        puts "</div>"
        puts "</div>"
    rescue
        puts "<meta http-equiv='refresh' content='10;url=select.cgi'>"
        puts "<title>ERROR</title></head>"
        puts "<body>"
        if pass_query == ""
            puts "<h2> You haven't given any conditionals </h2>"
        else
            puts "<h2>ERROR: There was an issue with the query, check conditionals</h2>"
        end
    end
else
    puts "<title>Select</title>"
    puts "</head>"
    puts "<body>"
    puts "<header class='header'>"
    puts "<h1>Select a Group of Data</h1>"
    puts "</header>"
    puts "<div class='content3'>"
    puts "<form method='post' action='select.cgi'>"

    puts "<legend>Please check all of the columns you would like to see in your Query. If you would like to see everything, leave all boxes unchecked<legend><br>"
    puts "<input type='checkbox' name='p_id' value= 'p.Passenger_ID' > Passenger_ID <br>"
    puts "<input type='checkbox' name='surv' value= 'p.Survive' > Survive <br>"
    puts "<input type='checkbox' name='honor' value= 'p.Honorific' > Honorific <br>"
    puts "<input type='checkbox' name='fName' value= 'p.First_Name' > First Name <br>"
    puts "<input type='checkbox' name='lName' value= 'p.Last_Name' > Last Name <br>"
    puts "<input type='checkbox' name='unName' value= 'p.Unmarried_Name' > Unmarried Name <br>"
    puts "<input type='checkbox' name='gndr' value= 'p.Gender' > Gender <br>"
    puts "<input type='checkbox' name='a' value= 'p.Age' > Age <br>"
    puts "<input type='checkbox' name='sos' value= 'f.Siblings_Or_Spouses' > Siblings/Spouses On Board <br>"
    puts "<input type='checkbox' name='pok' value= 'f.Parents_Or_Kids' > Parents/Kids On Board <br>"
    puts "<input type='checkbox' name='b_id' value= 'b.Boarding_ID' > Boarding_ID <br>"
    puts "<input type='checkbox' name='tNum' value= 'b.Ticket_Number' > Ticket_Number <br>"
    puts "<input type='checkbox' name='fre' value= 'b.Fare' > Fare <br>"
    puts "<input type='checkbox' name='cab' value= 'GROUP_CONCAT(c.Cabin ORDER BY c.Cabin SEPARATOR \", \") AS Cabins' > Cabins <br>"
    puts "<input type='checkbox' name='embfrm' value= 'b.Embarked_From' > Embarked From <br><br>"

    puts "<legend>Please fill out each text box with a conditional</legend>"
    puts "<h5>Rules: <br> If the right side of conditional is a word, surround with single quotes 'example' <br> Survive can either be True, False, or NULL"
    puts "<br>Conditional Options:<br> Equal To: = <br> Not Equal To: <> <br> Greater Than: > <br> Greater Than or Equal To: >= <br>"
    puts "<Less Than: < <br> Less Than or Equal To: <= <br> When a value is null: IS NULL <br> When a value isn't null: IS NOT NULL <br> Range: BETWEEN X AND Y<br>"
    puts "Examples: <br> Passenger_ID >= 50 <br> Embarked From = 'Southampton' <br> Age BETWEEN 30 AND 50 <br> Unmarried Name IS NULL <br> Survive = True<br>"
    puts "SPECIAL CASE: Cabins = 'C49', 'A6', 'B39' <br> Multple Cabins are always brought together by OR's </h5>"
    puts "Passenger_ID <input type='text' id='passenger_id' name='passenger_id' size ='15'><br>"
    puts "Survive <input type='text' id='survive' name='survive' size='15'><br>"
    puts "Honorific <input type='text' id='honorific' name='honorific' size ='15'><br>"
    puts "First Name <input type='text' id='firstName' name='firstName' size='15'><br>"
    puts "Last Name <input type='text' id='lastName' name='lastName' size='15'><br>"
    puts "Unmarried Name <input type='text' id='unmarriedName' name='unmarriedName' size='15'><br>"
    puts "Gender <input type='text' id='gender' name='gender' size='15'><br>"
    puts "Age <input type='text' id='age' name='age' size='15'><br>"
    puts "Siblings/Spouses On Board <input type='text' id='siblings' name='siblings' size='15'><br>"
    puts "Parents/Kids On Board <input type='text' id='parents' name='parents' size='15'><br>"
    puts "Boarding_ID <input type='text' id='boarding_id' name='boarding_id' size='15'><br>"
    puts "Class <input type='text' id='class' name='class' size='15'><br>"
    puts "Ticket Number <input type='text' id='ticketNumber' name='ticketNumber' size='15'><br>"
    puts "Fare <input type='text' id='fare' name='fare' size='15'><br>"
    puts "Cabins <input type='text' id='cabins' name='cabins' size='15'><br>"
    puts "Embarked From <input type='text' id='embarkedFrom' name='embarkedFrom' size='15'><br>"
    
    puts "<br><legend>Choose how you would like to connect your conditionals?</legend>"
    puts "<h5> AND will create a more specific query<br> OR will create a broader query</h5>"
    puts "<input type='radio' id='connector' name='connector' value=' AND ' checked > AND <br>"
    puts "<input type='radio' id='connector' name='connector' value=' OR ' > OR <br>"
    puts "<input type='hidden' id='submitted' name='submitted' value='true'>"
    puts "<br><input type='submit' value='Submit'>"
    puts "</form>"
    puts "</div>"
end
puts "</body>"
puts "</html>"