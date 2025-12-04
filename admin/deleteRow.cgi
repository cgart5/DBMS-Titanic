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
puts "<title>Delete</title></head>"

if cgi['passenger_id'] != ""
    # delete the tables that are dependent upon 
    # Cabins only populates when value is not empty in csv so some ID's don't have corresponding cabins
    begin
        db.query("DELETE FROM Cabins WHERE Passenger_ID = #{cgi['passenger_id']}; ")
    rescue
    end

    db.query("DELETE FROM Family_On_Board WHERE Passenger_ID = #{cgi['passenger_id']};")
    
    boarding_id = db.query("SELECT Boarding_ID FROM Passengers WHERE Passenger_ID = #{cgi['passenger_id']};")
    b_id = ""
    boarding_id.each() do |id|
        b_id = id['Boarding_ID']
    end
    db.query("DELETE FROM Passengers WHERE Passenger_ID = #{cgi['passenger_id']}; ")
    same_b_id = db.query("SELECT Passenger_ID FROM Passengers WHERE Boarding_ID = #{b_id};")

    # if there are multiple people with the same b_id then we keep it in the table if not we delete
    if same_b_id.count() == 0
        db.query("DELETE FROM Boarding_Info WHERE Boarding_ID = #{b_id};")
    end

    puts "<meta http-equiv='refresh' content='3;url=admin.cgi'>"
    puts "<title>DELETED</title></head>"
    puts "<body>"
    puts "<h2>Row was DELETED, you will be returned to Admin Options</h2>"     
else
    puts "<body>"
    puts "<h1>Please Select The Row You Would Like To Delete</h1>"
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
    puts "<th>Boarding_ID</th>"
    puts "<th>Class</th>"
    puts "<th>Ticket Number</th>"
    puts "<th>Fare</th>"
    puts "<th>Cabins</th>"
    puts "<th>Embarked From</th>"
    puts "<th>Delete This Row</th></tr>"
    puts "</thead>"
    puts "<tbody>"
    currentTable = db.query("SELECT p.Passenger_ID, p.Survive, p.Honorific, p.First_Name, p.Last_Name,p.Unmarried_Name, p.Gender, p.Age, f.Siblings_Or_Spouses, f.Parents_Or_Kids, b.Boarding_ID, b.Class, b.Ticket_Number, b.Fare, GROUP_CONCAT(c.Cabin ORDER BY c.Cabin SEPARATOR ', ') AS Cabins, b.Embarked_From FROM  Passengers p LEFT JOIN Family_On_Board f ON p.Passenger_ID = f.Passenger_ID LEFT JOIN Boarding_Info b ON p.Boarding_ID = b.Boarding_ID LEFT JOIN Cabins c ON p.Passenger_ID = c.Passenger_ID GROUP BY p.Passenger_ID;")
    currentTable.each() do |row|
        puts "<form action='deleteRow.cgi' method ='post'>"
        puts "<input type='hidden' name='passenger_id' value='#{row['Passenger_ID']}'>"
        #when position is 2, d[1] is BOOL
        position = 1
        puts "<tr>"
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
        puts "<td><input type='submit' value='DELETE'></td>"
        puts "</tr>"
        puts "</form>"
    end
    puts "</tbody>"
    puts "</table>"
    puts "</div>"
end
puts "</body>"
puts "</html>"