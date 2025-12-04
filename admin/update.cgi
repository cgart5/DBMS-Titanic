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
puts "<title>Update</title></head>"

if cgi['updateType'] == 'passengerInfo'
    if cgi['submitted'] == 'true'
        #Passengers Table
        pass_query = ""
        if cgi['survive'] != ""
            pass_query = "Survive = #{cgi['survive']}"
        end
        if cgi['honorific'] != ""
            if pass_query != ""
                pass_query = pass_query + ", Honorifc = #{cgi['honorific']}"
            else
                pass_query = "Honorific = #{cgi['honorific']}"
            end
        end
        if cgi['firstName'] != ""
            if pass_query != ""
                pass_query = pass_query + ", First_Name = #{cgi['firstName']}"
            else
                pass_query = "First_Name = #{cgi['firstName']}"
            end
        end
        if cgi['lastName'] != ""
            if pass_query != ""
                pass_query = pass_query + ", Last_Name = #{cgi['lastName']}"
            else
                pass_query = "Last_Name = #{cgi['lastName']}"
            end
        end
        if cgi['unmarriedName'] != ""
            if pass_query != ""
                pass_query = pass_query + ", Unmarried_Name = #{cgi['unmarriedName']}"
            else
                pass_query = "Unmarried_Name = #{cgi['unmarriedName']}"
            end
        end
        if cgi['gender'] != ""
            if pass_query != ""
                pass_query = pass_query + ", Gender = #{cgi['gender']}"
            else
                pass_query = "Gender = #{cgi['gender']}"
            end
        end
        if cgi['age'] != ""
            if pass_query != ""
                pass_query = pass_query + ", Age = #{cgi['age']}"
            else
                pass_query = "Age = #{cgi['age']}"
            end
        end
        
        #Family on board table
        fam_query = ""
        if cgi['siblings'] != ""
            fam_query = "Siblings_Or_Spouses = #{cgi['siblings']}"
        end

        if cgi['parents'] != ""
            if fam_query != ""
                fam_query = fam_query + ", Parents_Or_Kids = #{cgi['parents']}"
            else
                fam_query = "Parents_Or_Kids = #{cgi['parents']}"
            end
        end

        #Cabins table
        cabins = []
        if cgi['cabins'] != ""
            cabins = cgi['cabins'].strip().split(',')
        end
        
        #if one query fails none of them update
        begin
            if pass_query != ""
                db.query("UPDATE Passengers SET #{pass_query} WHERE Passenger_ID = #{cgi['passenger_id']};")
            end
            if fam_query != ""
                db.query("UPDATE Family_On_Board SET #{fam_query} WHERE Passenger_ID = #{cgi['passenger_id']};")
            end
            if cgi['cabins'] != ""
                db.query("DELETE FROM Cabins WHERE Passenger_ID = #{cgi['passenger_id']};")
                cabins.each() do |cabin|
                    db.query("INSERT INTO Cabins VALUES(#{cgi['passenger_id']}, #{cabin});")
                end
            end
            puts "<meta http-equiv='refresh' content='3;url=admin.cgi'>"
            puts "<title>UPDATED</title></head>"
            puts "<body>"
            puts "<h2>Row was Updated, you will be returned to Admin Options</h2>"
        rescue => e
            puts "<meta http-equiv='refresh' content='3;url=update.cgi'>"
            puts "<title>ERROR</title></head>"
            puts "<body>"
            puts "<h2>ERROR: There was an issue with the query, check conditionals</h2>"
        end
    elsif cgi['passenger_id'] != ""
        puts "<body>"
        puts "<header class='header'>"
        puts "<h1>Update Conditions</h1>"
        puts "<h2>Updating Passenger_ID: #{cgi['passenger_id']}</h2>"
        puts "</header>"
        puts "<div class='content2'>"
        puts "<form method='post' action='update.cgi'>"
        puts "<legend>Please fill out each text box with a condition:</legend>"
        puts "<h5>If the right side of conditional is a word, surround with single quotes 'example'"
        puts "<br>Conditional Options:<br> All text boxs are set equal to column automatically <br> When a value is null: NULL<br>"
        puts "Examples: <br> Age: 50 <br> Embarked From: 'Southampton' <br> Unmarried Name: NULL <br>"
        puts "SPECIAL CASE: Cabins: 'C49', 'G6' , 'F9' </h5>"
        puts "Survive <input type='text' id='survive' name='survive' size='15><br>"
        puts "Honorific <input type='text' id='honorific' name='honorific' size ='15'><br>"
        puts "First Name <input type='text' id='firstName' name='firstName' size='15'><br>"
        puts "Last Name <input type='text' id='lastName' name='lastName' size='15'><br>"
        puts "Unmarried Name <input type='text' id='unmarriedName' name='unmarriedName' size='15'><br>"
        puts "Gender <input type='text' id='gender' name='gender' size='15'><br>"
        puts "Age <input type='text' id='age' name='age' size='15'><br>"
        puts "Siblings/Spouses On Board <input type='text' id='siblings' name='siblings' size='15'><br>"
        puts "Parents/Kids On Board <input type='text' id='parents' name='parents' size='15'><br>"
        puts "Cabins <input type='text' id='cabins' name='cabins' size='15'><br>"
        puts "<input type='hidden' id='submitted' name='submitted' value='true'>"
        puts "<input type='hidden' id='updateType' name='updateType' value='#{cgi['updateType']}'>"
        puts "<input type='hidden' id='passenger_id' name='passenger_id' value='#{cgi['passenger_id']}'>"
        puts "<br><input type='submit' value='Submit'>"
        puts "</form>"
        puts "</div>"
    else
        puts "<body>"
        puts "<h1>Please Select The Row You Would Like To Update</h1>"
        puts "<h2>Scroll To The Left To Submit</h2>"
        puts "<div class='scroll-container'>"
        puts "<div class='table-panel'>"
        puts "<table class='db'><tr>"
        puts "<caption>Titanic Passengers</caption>"
        puts "<thead>"
        puts "<th>Passenger_ID</th>"
        puts "<th>Survive</th>"
        puts "<th>Honorific</th>"
        puts "<th>First Name</th>"
        puts "<th>Last Name</th>"
        puts "<th>Unmarried Name</th>"
        puts "<th>Gender</th>"
        puts "<th>Age</th>"
        puts "<th>Siblings/Spouses On Board</th>"
        puts "<th>Parents/Kids On Board</th>"
        puts "<th>Cabins</th>"
        puts "<th>Update This Row</th></tr>" 
        puts "</thead>"
        puts "<tbody>"
        currentTable = db.query("SELECT p.Passenger_ID, p.Survive, p.Honorific, p.First_Name, p.Last_Name,p.Unmarried_Name, p.Gender, p.Age, f.Siblings_Or_Spouses, f.Parents_Or_Kids, GROUP_CONCAT(c.Cabin ORDER BY c.Cabin SEPARATOR ', ') AS Cabins FROM  Passengers p LEFT JOIN Family_On_Board f ON p.Passenger_ID = f.Passenger_ID LEFT JOIN Cabins c ON p.Passenger_ID = c.Passenger_ID GROUP BY p.Passenger_ID;")
        currentTable.each() do |row|
            puts "<form action='update.cgi' method ='post'>"
            puts "<input type='hidden' name='passenger_id' value='#{row['Passenger_ID']}'>"
            puts "<input type='hidden' name='updateType' value='passengerInfo'>"
            puts "<tr>"
            #when position is 2, d[1] is BOOL
            position = 1
            row.each() do |d|
                if d[1] == nil
                    puts "<td>NULL</td>"
                elsif d[1] == 0 && position == 2
                    puts "<td>False</td>"
                elsif d[1] == 1 && position == 2
                    puts "<td>True</td>"
                else
                    puts "<td>#{d[1]}</td>" 
                end 
                position += 1
            end
            puts "<td><input type='submit' value='UPDATE'></td>"
            puts "</tr>"
            puts "</form>"
        end
        puts "</tbody>"
        puts "</table>"
        puts "</div>"
    end
elsif cgi['updateType'] == 'boardingInfo'
    if cgi['submitted'] == 'true'
        #Boarding_Info Table
        board_query = ""
        if cgi['class'] != ""
            board_query = "Class = #{cgi['class']}"
        end
        if cgi['ticketNumber'] != ""
            if board_query != ""
                board_query = board_query + ", Ticket_Number = #{cgi['ticketNumber']}"
            else
                board_query = "Ticket_Number = #{cgi['ticketNumber']}"
            end
        end
        if cgi['fare'] != ""
            if board_query != ""
                board_query = board_query + ", Fare = #{cgi['fare']}"
            else
                board_query = "Fare = #{cgi['fare']}"
            end
        end
        if cgi['embarkedFrom'] != ""
            if board_query != ""
                board_query = board_query + ", Embarked_From = #{cgi['embarkedFrom']}"
            else
                board_query = "Embarked_From = #{cgi['embarkedFrom']}"
            end
        end

        #if one query fails none of them update
        begin
            if board_query != ""
                db.query("UPDATE Boarding_Info SET #{board_query} WHERE Boarding_ID = #{cgi['boarding_id']};")
            end
            puts "<meta http-equiv='refresh' content='3;url=admin.cgi'>"
            puts "<title>UPDATED</title></head>"
            puts "<body>"
            puts "<h2>Row was Updated, you will be returned to Admin Options</h2>"
        rescue => e
            puts "<meta http-equiv='refresh' content='3;url=update.cgi'>"
            puts "<title>ERROR</title></head>"
            puts "<body>"
            puts "<h2>ERROR: There was an issue with the query, check conditionals</h2>"
        end
    elsif cgi['boarding_id'] != ""
        puts "<body>"
        puts "<header class='header'>"
        puts "<h1>Update Conditions</h1>"
        puts "<h2>Updating Boarding_ID: #{cgi['boarding_id']}</h2>"
        puts "</header>"
        puts "<div class='content2'>"
        puts "<form method='post' action='update.cgi'>"
        puts "<legend>Please fill out each text box with a condition:</legend>"
        puts "<h5>If the right side of conditional is a word, surround with single quotes 'example'"
        puts "<br>If value stays the same, leave blank"
        puts "<br>Conditional Options:<br> Equal To: = <br> When a value is null: = NULL<br>"
        puts "Examples: <br> Age = 50 <br> Embarked From = 'Southampton' <br> Fare = NULL </h5>"
        puts "Class <input type='text' id='class' name='class' size='15'><br>"
        puts "Ticket Number <input type='text' id='ticketNumber' name='ticketNumber' size='15'><br>"
        puts "Fare <input type='text' id='fare' name='fare' size='15'><br>"
        puts "Embarked From <input type='text' id='embarkedFrom' name='embarkedFrom' size='15'><br>"
        puts "<input type='hidden' id='submitted' name='submitted' value='true'>"
        puts "<input type='hidden' id='updateType' name='updateType' value='#{cgi['updateType']}'>"
        puts "<input type='hidden' id='passenger_id' name='boarding_id' value='#{cgi['boarding_id']}'>"
        puts "<br><input type='submit' value='Submit'>"
        puts "</form>"
        puts "</div>"
    else
        puts "<body>"
        puts "<h1>Please Select The Row You Would Like To Update</h1>"
        puts "<div class='scroll-container'>" 
        puts "<div class='table-panel'>"
        puts "<table class='db'><tr>"
        puts "<caption>Boarding_Info</caption>"
        puts "<thead>"
        puts "<th>Boarding_ID</th>"
        puts "<th>Class</th>"
        puts "<th>Ticket Number</th>"
        puts "<th>Fare</th>"
        puts "<th>Embarked From</th>"
        puts "<th>Update This Row</th></tr>"
        puts "</thead>"
        puts "<tbody>"
        currentTable = db.query("SELECT * FROM Boarding_Info;")
        currentTable.each() do |row|
            puts "<form action='update.cgi' method ='post'>"
            puts "<input type='hidden' name='boarding_id' value='#{row['Boarding_ID']}'>"
            puts "<input type='hidden' name='updateType' value='boardingInfo'>"
            puts "<tr>"
            row.each() do |d|
                if d[1] == nil
                    puts "<td>NULL</td>"
                else
                    puts "<td>#{d[1]}</td>" 
                end 
            end
            puts "<td><input type='submit' value='UPDATE'></td>"
            puts "</tr>"
            puts "</form>"
        end
        puts "</tbody>"
        puts "</table>"
        puts "</div>"
        puts "</div>"
    end
else
    puts "<title>Update Options</title>"
    puts "</head>"
    puts "<body>"
    puts "<header class='header'>"
    puts "<h1>Update Options</h1>"
    puts "<h2>Titanic Tables</h2>"
    puts "</header>"
    puts "<div class='content3'>"
    puts "<form method='post' action='update.cgi'>"
    puts "<legend>Which table set would you like to update?</legend>"
    puts "<h5>If wanting to update information a part of Passenger Info and Boarding Info, delete row and then insert</h5>"
    puts "<input type='radio' name='updateType' value='passengerInfo' checked> Passenger Info(Passengers, Family_On_Board, and Cabins) <br>"
    puts "<input type='radio' name='updateType' value='boardingInfo'> Boarding Info Table<br>"
    puts "<input type ='hidden' id='decision' name ='decision' value = "">"
    puts "<br><input type='submit' value='Submit'>"
    puts "</form>"
    puts "</div>"
end
puts "</body>"
puts "</html>"
