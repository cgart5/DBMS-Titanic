#!/usr/bin/ruby

# DELETE WITH JOIN: https://stackoverflow.com/questions/652770/delete-with-join-in-mysql

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

if cgi['submitted'] == 'true'
    #interpret form
    #passenger table
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
            pass_query = pass_query + "#{cgi['connector']} p.Unmarried #{cgi['unmarriedName'].strip()} "
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

    #family table
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
    
    #boarding table
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

    #cabins table
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
            cabin_query = cabin_query + ")"
            pass_query = pass_query + "AND #{cabin_query}"  
        end
    end
    
    begin
        valid_b_id = db.query("SELECT b.Boarding_ID FROM  Passengers p LEFT JOIN Family_On_Board f ON p.Passenger_ID = f.Passenger_ID LEFT JOIN Boarding_Info b ON p.Boarding_ID = b.Boarding_ID LEFT JOIN Cabins c ON p.Passenger_ID = c.Passenger_ID WHERE #{pass_query};")
        list_of_b_id = []
        invalid_b_id = []
        valid_b_id.each() do |b_id|
            list_of_b_id.each() do |b|
                if b == b_id['Boarding_ID']
                    invalid_b_id.push(b)
                end
            end
            list_of_b_id.push(b_id['Boarding_ID'])
        
            p_id = db.query("SELECT Passenger_ID FROM Passengers WHERE Boarding_ID = #{b_id['Boarding_ID']};")

            # if there is only one or possibly no more passengers with that boarding info we delete that information  
            if p_id.count() == 1
                invalid_b_id.push(b_id['Boarding_ID'])
            end
        end
        
        db.query("DELETE p FROM Passengers p LEFT JOIN Family_On_Board f ON p.Passenger_ID = f.Passenger_ID LEFT JOIN Boarding_Info b ON p.Boarding_ID = b.Boarding_ID LEFT JOIN Cabins c ON p.Passenger_ID = c.Passenger_ID WHERE #{pass_query};")
        invalid_b_id.each() do |b_id|
            begin
                db.query("DELETE FROM Boarding_Info WHERE Boarding_ID = #{b_id};")
            rescue
                #accidental duplicate in invalid_b_id
            end
        end
        puts "<meta http-equiv='refresh' content='3;url=admin.cgi'>"
        puts "<title>DELETED</title></head>"
        puts "<body>"
        puts "<h2>Rows were DELETED, you will be returned to Admin Options</h2>"
    rescue => e
        puts "<meta http-equiv='refresh' content='3;url=deleteRows.cgi'>"
        puts "<title>ERROR</title></head>"
        puts "<body>"
        puts "<h2>ERROR: There was an issue with the query, check conditionals</h2>"
    end
else
    puts "<title>Delete</title>"
    puts "</head>"
    puts "<body>"
    puts "<header class='header'>"
    puts "<h1>Delete Conditions</h1>"
    puts "<h2>Titanic Tables</h2>"
    puts "</header>"
    puts "<div class='content2'>"
    puts "<form method='post' action='deleteRows.cgi'>"
    puts "<legend>Please fill out each text box with a conditional</legend>"
    puts "<h5>Rules: <br>If right side of the conditional is a word please surround with single quotes <br> Survive can either be True, False, or NULL <br> Conditional Options:<br> Equal To: = <br> Not Equal To: <> <br> Greater Than: > <br> Greater Than or Equal To: >= <br>"
    puts "<Less Than: < <br> Less Than or Equal To: <= <br> When a value is null: IS NULL <br> When a value isn't null: IS NOT NULL <br> Range: BETWEEN X AND Y<br>"
    puts "Examples: <br> Passenger_ID >= 50 <br> Embarked From = 'Southampton' <br> Age BETWEEN 30 AND 50 <br> Unmarried Name IS NULL<br>"
    puts "SPECIAL CASE: Cabins = 'C49', 'A6', 'B39' <br> Multple Cabins are always brought together by OR's </h5>"   
    puts "Passenger_ID <input type='text' id='passenger'_id name='passenger_id' size ='15'><br>"
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
    puts "<input type='radio' id='connector' name='connector' value=' OR '  > OR <br>"
    puts "<input type='hidden' id='submitted' name='submitted' value='true'>"
    puts "<br><input type='submit' value='Submit'>"
    puts "</form>"
    puts "</div>"
end
puts "</body>"
puts "</html>" 