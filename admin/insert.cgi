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
puts "<title>Insert</title></head>"

if cgi['submitted'] == 'true'
    # String Build for insertion
    passengers = ""
    family_on_board = ""
    boarding_info = ""
    cabins = ""
    p_id_query = ""
    b_id_query = ""

    if cgi['survive'] == "True"
        passengers = "TRUE,"
        p_id_query = "Survive = 1 AND "
    elsif cgi['survive'] == "False"
        passengers = "FALSE,"
        p_id_query = "Survive = 0 AND "
    else
        passengers = "NULL,"
        p_id_query = "Survive IS NULL AND "
    end
    if cgi['class'] != ""
        boarding_info = "#{cgi['class']},"
        b_id_query = "Class = #{cgi['class']} AND "
    else
        boarding_info = "NULL,"
        b_id_query = "Class IS NULL AND "

    end
    if cgi['honorific'] != ""
        passengers = passengers + "'#{cgi['honorific']}',"
        p_id_query = p_id_query + "Honorific = '#{cgi['honorific']}' AND "
    else
        passengers = passengers + "NULL,"
        p_id_query = p_id_query + "Honorific IS NULL AND "
    end
    if cgi['firstName'] != ""
        passengers = passengers + "\"#{cgi['firstName']}\","
        p_id_query = p_id_query + "First_Name = \"#{cgi['firstName']}\" AND "
    else
        passengers = passengers + "NULL,"
        p_id_query = p_id_query + "First_Name IS NULL AND "
    end
    if cgi['lastName'] != ""
        passengers = passengers + "\"#{cgi['lastName']}\","
        p_id_query = p_id_query + "Last_Name = \"#{cgi['lastName']}\" AND "
    else
        passengers = passengers + "NULL,"
        p_id_query = p_id_query + "Last_Name IS NULL AND "
    end
    if cgi['unmarriedName'] != ""
        passengers = passengers + "\"#{cgi['unmarriedName']}\","
        p_id_query = p_id_query + "Unmarried_Name = \"#{cgi['unmarriedName']}\" AND "
    else
        passengers = passengers + "NULL,"
        p_id_query = p_id_query + "Unmarried_Name IS NULL AND "
    end
    if cgi['gender'] != ""
        passengers = passengers + "'#{cgi['gender']}',"
        p_id_query = p_id_query + "Gender = '#{cgi['gender']}' AND "
    else
        passengers = passengers + "NULL,"
        p_id_query = p_id_query + "Gender IS NULL AND "
    end
    if cgi['age'] != ""
        passengers = passengers + "'#{cgi['age']}',"
        p_id_query = p_id_query + "Age = #{cgi['age']} AND "
    else
        passengers = passengers + "NULL,"
        p_id_query = p_id_query + "Age IS NULL AND "
    end
    if cgi['siblings'] != ""
        family_on_board = "#{cgi['siblings']},"
    else
        family_on_board = "NULL,"
    end
    if cgi['parents'] != ""
        family_on_board = family_on_board + "#{cgi['parents']}"
    else
        family_on_boardn = family_on_board + "NULL"
    end
    if cgi['ticketNumber'] != ""
        boarding_info = boarding_info + "#{cgi['ticketNumber']},"
        b_id_query = b_id_query + "Ticket_Number = #{cgi['ticketNumber']} AND "
    else
        boarding_info = boarding_info + "NULL,"
        b_id_query = b_id_query + "Ticket_Number IS NULL AND "
    end
    if cgi['fare'] != ""
        boarding_info = boarding_info + "#{cgi['fare']},"
        b_id_query = b_id_query + "Fare = #{cgi['fare']} AND "
    else
        boarding_info = boarding_info + "NULL,"
        b_id_query = b_id_query + "Fare IS NULL AND "
    end
    if cgi['embarkedFrom'] != ""
        boarding_info = boarding_info + "\"#{cgi['embarkedFrom']}\""
        b_id_query = b_id_query + "Embarked_From = \"#{cgi['embarkedFrom']}\""
    else
        boarding_info = boarding_info + "NULL"
        b_id_query = b_id_query + "Embarked_From IS NULL"
    end

    begin
        boarding_id = db.query("SELECT Boarding_ID FROM Boarding_Info WHERE #{b_id_query};")
        #if the boarding id already exists we use that one for the new entry if not, we make a new one
        if boarding_id.count() == 0
            db.query("INSERT INTO Boarding_Info(Class,Ticket_Number,Fare,Embarked_From) VALUES(#{boarding_info});")
        end

        #query done again in case there wasn't an existing id and then that one would be selected
        boarding_id = db.query("SELECT Boarding_ID FROM Boarding_Info WHERE #{b_id_query};")
        boarding_id.each() do |id|
            passengers = passengers + id['Boarding_ID'].to_s
            p_id_query = p_id_query + "Boarding_ID = #{id['Boarding_ID']}"
        end

        db.query("INSERT INTO Passengers(Survive, Honorific, First_Name, Last_Name, Unmarried_Name, Gender, Age, Boarding_ID) VALUES(#{passengers});")
        passenger_id = db.query("SELECT Passenger_ID FROM Passengers WHERE #{p_id_query};")
        
        p_id = ""
        passenger_id.each() do |id|
            p_id = id['Passenger_ID'].to_s
        end

        db.query("INSERT INTO Family_On_Board VALUES(#{p_id}, #{family_on_board});")

        if cgi['cabins'] != ""
            cabins = cgi['cabins'].split()
            cabins.each() do |cabin|
                db.query("INSERT INTO Cabins VALUES(#{p_id}, '#{cabin}')")
            end
        else
            #is null not inserted
        end
        puts "<meta http-equiv='refresh' content='3;url=admin.cgi'>"
        puts "<title>INSERTED</title></head>"
        puts "<body>"
        puts "<h2>Rows was inserted, you will be returned to Admin Options</h2>"
    rescue 
        puts "<meta http-equiv='refresh' content='3;url=insert.cgi'>"
        puts "<title>ERROR</title></head>"
        puts "<body>"
        puts "<h2>ERROR: There was an issue with the query, check conditionals</h2>"
    end
else
    puts "<body>"
    puts "<header class='header'>"
    puts "<h1>Insert New Row</h1>"
    puts "</header>"
    puts "<div class='content2'>"
    puts "<form method='post' action='insert.cgi'>"
    puts "<legend>Please state what each column is equal to:</legend>"
    puts "<h5>Rules: <br> If the textbox contains a word it does not need quotes"
    puts "<br>Leave Blank if NULL"
    puts "<br>If Cabins has mutliple values, seperate by spaces"
    puts "<br>Survive can either be False, True, or NULL, no quotes <br>"
    puts "<br>Examples: <br> Age: 50 <br> Embarked From:Southampton <br> Cabins: A20 B30 C40 <br> Survive: False</h5>"
    puts "Survive:<input type='text' id='survive' name='survive' size='12'><br>"  
    puts "Honorific: <input type='text' id='honorific' name='honorific' size ='12'><br>"
    puts "First Name:<input type='text' id='firstName' name='firstName' size='12'><br>"
    puts "Last Name: <input type='text' id='lastName' name='lastName' size='12'><br>"
    puts "Unmarried Name: <input type='text' id='unmarriedName' name='unmarriedName' size='12'><br>"
    puts "Gender: <input type='text' id='gender' name='gender' size='12'><br>"
    puts "Age: <input type='text' id='age' name='age' size='12'><br>"
    puts "Siblings/Spouses On Board: <input type='text' id='siblings' name='siblings' size='12'><br>"
    puts "Parents/Kids On Board: <input type='text' id='parents' name='parents' size='12'><br>"
    puts "Class: <input type='text' id='class' name='class' size='12'><br>"
    puts "Ticket Number: <input type='text' id='ticketNumber' name='ticketNumber' size='12'><br>"
    puts "Fare: <input type='text' id='fare' name='fare' size='12'><br>"
    puts "Cabins: <input type='text' id='cabins' name='cabins' size='12'><br>"
    puts "Embarked From: <input type='text' id='embarkedFrom' name='embarkedFrom' size='12'><br>"
    puts "<input type='hidden' id='submitted' name='submitted' value='true'>"
    puts "<br><input type='submit' value='Submit'>"
    puts "</form>"
    puts "</div>"
end
puts "</body>"
puts "</html>"