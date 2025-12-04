#!/usr/bin/ruby

#Group Concat Function: https://www.naukri.com/code360/library/groupconcat-function-in-mysql

$stdout.sync = true
$stderr.reopen $stdout

print "content-type: text/html\r\n\r\n"

require 'cgi'
require 'stringio'
require 'mysql2'

cgi = CGI.new("html5")

puts "<html>"
puts "<head>"
puts "<link rel='stylesheet'; href='styles.css'>"

db = Mysql2::Client.new(:host=>'_____',:username=> '___',:password => '___', :database=> '____')

if cgi['decision'] == "seperate"
    puts "<title>Tables</title></head>"
    puts "<body>"
    puts "<form method='post' action='basicUser.cgi' class='upload-form'>"
    puts "<button type='submit' class='upload-button'>Make Another Query</button>"
    puts "</form>"
    puts "<div class='scroll-container'>"

    #Print Passenger Table
    puts "<div class='table-panel'>"
    puts "<table class='db'><tr>"
    puts "<caption>Passengers</caption>"
    puts "<thead>"
    puts "<th>Passenger_ID</th>"
    puts "<th>Survive</th>"
    puts "<th>Honorific</th>"
    puts "<th>First Name</th>"
    puts "<th>Last Name</th>"
    puts "<th>Unmarried Name</th>"
    puts "<th>Gender</th>"
    puts "<th>Age</th>"
    puts "<th>Boarding_ID</th><tr>"
    puts "</thead>"
    puts "<tbody>"
    currentTable = db.query("SELECT * FROM Passengers;")
    currentTable.each() do |row|
        puts "<tr>"
        row.each() do |d|
            if d[1] == nil
                puts "<td>NULL</td>"
            elsif d[1] == 0
                puts "<td>False</td>"
            elsif d[1] == 1
                puts "<td>True</td>"
            else
                puts "<td>#{d[1]}</td>" 
            end 
        end
        puts "</tr>"
    end
    puts "</tbody>"
    puts "</table>"
    puts "</div>"

    #Print Family_On_Board Table
    puts "<div class='table-panel'>"
    puts "<table class='db'><tr>"
    puts "<caption>Family_On_Board</caption>"
    puts "<thead>"
    puts "<th>Passenger_ID</th>"
    puts "<th>Siblings/Spouses On Board</th>"
    puts "<th>Parents/Kids On Board</th></tr>"
    puts "</thead>"
    puts "<tbody>"
    currentTable = db.query("SELECT * FROM Family_On_Board;")
    currentTable.each() do |row|
        puts "<tr>"
        row.each() do |d|
            if d[1] == nil
                puts "<td>NULL</td>"
            else
                puts "<td>#{d[1]}</td>" 
            end 
        end
        puts "</tr>"
    end
    puts "</tbody>"
    puts "</table>"
    puts "</div>"

    #Print Cabins
    puts "<div class='table-panel'>"
    puts "<table class='db'><tr>"
    puts "<caption>Cabins</caption>"
    puts "<thead>"
    puts "<th>Passenger_ID</th>"
    puts "<th>Cabin</th><tr>"
    puts "</thead>"
    puts "<tbody>"
    currentTable = db.query("SELECT * FROM Cabins;")
    currentTable.each() do |row|
        puts "<tr>"
        row.each() do |d|
            if d[1] == nil
                puts "<td>NULL</td>"
            else
                puts "<td>#{d[1]}</td>" 
            end 
        end
        puts "</tr>"
    end
    puts "</tbody>"
    puts "</table>"
    puts "</div>"

    #Print Boarding_Info
    puts "<div class='table-panel'>"
    puts "<table class='db'><tr>"
    puts "<caption>Boarding_Info</caption>"
    puts "<thead>"
    puts "<th>Boarding_ID</th>"
    puts "<th>Class</th>"
    puts "<th>Ticket Number</th>"
    puts "<th>Fare</th>"
    puts "<th>Embarked From</th><tr>"
    puts "</thead>"
    puts "<tbody>"
    currentTable = db.query("SELECT * FROM Boarding_Info;")
    currentTable.each() do |row|
        puts "<tr>"
        row.each() do |d|
            if d[1] == nil
                puts "<td>NULL</td>"
            else
                puts "<td>#{d[1]}</td>" 
            end 
        end
        puts "</tr>"
    end
    puts "</tbody>"
    puts "</table>"
    puts "</div>"
    puts "</div>"
elsif cgi['decision'] == "joined"
    puts "<title>Table</title></head>"
    puts "<body>"
    puts "<form method='post' action='basicUser.cgi' class='upload-form'>"
    puts "<button type='submit' class='upload-button'>Make Another Query</button>"
    puts "</form>"
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
    puts "<th>Embarked From</th><tr>"
    puts "</thead>"
    puts "<tbody>"
    currentTable = db.query("SELECT p.Passenger_ID, p.Survive, p.Honorific, p.First_Name, p.Last_Name,p.Unmarried_Name, p.Gender, p.Age, f.Siblings_Or_Spouses, f.Parents_Or_Kids, b.Boarding_ID, b.Class, b.Ticket_Number, b.Fare, GROUP_CONCAT(c.Cabin ORDER BY c.Cabin SEPARATOR ', ') AS Cabins, b.Embarked_From FROM  Passengers p LEFT JOIN Family_On_Board f ON p.Passenger_ID = f.Passenger_ID LEFT JOIN Boarding_Info b ON p.Boarding_ID = b.Boarding_ID LEFT JOIN Cabins c ON p.Passenger_ID = c.Passenger_ID GROUP BY p.Passenger_ID;")
    currentTable.each() do |row|
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
        puts "</tr>"
    end
    puts "</tbody>"
    puts "</table>"
    puts "</div>"
else
    puts "<title>View Type</title></head>"
    puts "<body>"
    puts "<header class='header'>"
    puts "<h1>Choose Your View</h1>"
    puts "</header>"
    puts "<div class='content'>"
    puts "<form method='post' action='viewAll.cgi'>"
    puts "<legend>How would you like the Data Displayed?</legend><br>"
    puts "<input type='radio' name='decision' value='seperate' checked> Seperate Tables <br>"
    puts "<input type='radio' name='decision' value='joined' > Joined Table <br><br>"
    puts "<input type='submit'>"
    puts "</form>"
end
puts "</body>"
puts "</html>"