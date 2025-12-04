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
    #build selected items list
    p_column_list = []
    p_query = ""
    if cgi['p_id'] != ""
        p_query = "#{cgi['operation']}(DISTINCT #{cgi['p_id']})"
        p_column_list.push("Passenger_ID")
    end
    
    if cgi['surv'] != ""
        if p_query == ""
            p_query = "#{cgi['operation']}(#{cgi['surv']})"
        else
            p_query = p_query + ",#{cgi['operation']}(#{cgi['surv']})"
        end
        p_column_list.push("Survive")
    end

    if cgi['a'] != ""
        if p_query == ""
            p_query = "#{cgi['operation']}(#{cgi['a']})"
        else
            p_query = p_query + ",#{cgi['operation']}(#{cgi['a']})"
        end
        p_column_list.push("Age")
    end

    if cgi['sos'] != ""
        if p_query == ""
            p_query = "#{cgi['operation']}(#{cgi['sos']})"
        else
            p_query = p_query + ",#{cgi['operation']}(#{cgi['sos']})"
        end
        p_column_list.push("Siblings/Spouses On Board")
    end

    if cgi['pok'] != ""
        if p_query == ""
            p_query = "#{cgi['operation']}(#{cgi['pok']})"
        else
            p_query = p_query + ",#{cgi['operation']}(#{cgi['pok']})"
        end
        p_column_list.push("Parents/Kids On Board")
    end
    b_query = ""
    b_column_list = []
    if cgi['b_id'] != ""
        if b_query == ""
            b_query = "#{cgi['operation']}(DISTINCT #{cgi['b_id']})"
        else
            b_query = b_query + ",#{cgi['operation']}(#{cgi['b_id']})"
        end
        b_column_list.push("Boarding_ID")
    end

    if cgi['tNum'] != ""
        if b_query == ""
            b_query = "#{cgi['operation']}(#{cgi['tNum']})"
        else
            b_query = b_query + ",#{cgi['operation']}(#{cgi['tNum']})"
        end
        b_column_list.push("Ticket Number")
    end
    if cgi['cls'] != ""
        if b_query == ""
            b_query = "#{cgi['operation']}(#{cgi['cls']})"
        else
            b_query = b_query + ",#{cgi['operation']}(#{cgi['cls']})"
        end
        b_column_list.push("Class")
    end

    if cgi['fre'] != ""
        if b_query == ""
            b_query = "#{cgi['operation']}(#{cgi['fre']})"
        else
            b_query = b_query + ",#{cgi['operation']}(#{cgi['fre']})"
        end
        b_column_list.push("Fare")
    end

    #build conditional part of the query
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
    
    board_query = ""
    if cgi['ticketNumber'] != ""
        if board_query == ""
            board_query = "p.Ticket_Number #{cgi['ticketNumber'].strip()} "
        else
            board_query = board_query + "#{cgi['connector']} p.Ticket_Number #{cgi['ticketNumber'].strip()} "
        end
    end
    if cgi['class'] != ""
        if board_query == ""
            board_query = "p.Class #{cgi['class'].strip()} "
        else
            board_query = board_query + "#{cgi['connector']} p.Class #{cgi['class'].strip()} "
        end
    end
    if cgi['fare'] != ""
        if board_query == ""
            board_query = "p.Fare #{cgi['fare'].strip()} "
        else
            board_query = board_query + "#{cgi['connector']} p.Fare #{cgi['fare'].strip()} "
        end
    end 
    if cgi['embarkedFrom'] != ""
        if board_query == ""
            board_query = "p.Embarked_From #{cgi['embarkedFrom'].strip()} "
        else
            board_query = board_query + "#{cgi['connector']} p.Embarked_From #{cgi['embarkedFrom'].strip()} "
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
            cabin_query = cabin_query + ")"
            if pass_query != ""
                pass_query = pass_query + "#{cgi['connector']} #{cabin_query}" 
            else
                pass_query = cabin_query
            end
        end
    end

    puts "<title>Query</title>"
    puts "</head>"
    puts "<header class='header'>"
    puts "<h1>Here are your calculations:</h1>"
    puts "<h3>p.Attribute is just an attribute coming from a joined table </h3>"
    puts "</header>"
    puts "<form method='post' action='admin.cgi' class='upload-form'>"
    puts "<button type='submit' class='upload-button'>Make Another Query</button>"
    puts "</form>"
    puts "<div class=content2>"
    puts "<form>"
    # p is chosen for name of every table in select besides cabins in case that Boarding_Info is wanted, which can appear in either table
    # no conditional
    begin
        if pass_query == "" && board_query == ""
            if p_query != ""
                currentOp = db.query("SELECT #{p_query} FROM Passengers p LEFT JOIN Family_On_Board f ON p.Passenger_ID = f.Passenger_ID LEFT JOIN Cabins c ON p.Passenger_ID = c.Passenger_ID;")
                currentOp.each() do |op|
                    op.values.zip(p_column_list).each() do |val, col|
                        puts "<h2> The #{cgi['operation']} of #{col} is #{val.round(2)}"
                    end
                end
            elsif b_query != ""
                currentOp = db.query("SELECT #{b_query} FROM  Boarding_Info p;")
                currentOp.each() do |op|
                    op.values.zip(b_column_list).each() do |val, col|
                        puts "<h2> The #{cgi['operation']} of #{col} #{val.round(2)}"
                    end
                end
            else
                puts "<h2>No calculations made</h2>"
            end
        # conditional only apart of passenger tables
        elsif pass_query != "" && board_query == ""
            if p_query != ""
                currentOp = db.query("SELECT #{p_query} FROM Passengers p LEFT JOIN Family_On_Board f ON p.Passenger_ID = f.Passenger_ID LEFT JOIN Cabins c ON p.Passenger_ID = c.Passenger_ID WHERE #{pass_query};")
                currentOp.each() do |op|
                    op.values.zip(p_column_list).each() do |val, col|
                        puts "<h2> The #{cgi['operation']} of #{col} Where #{pass_query} is #{val.round(2)}"
                    end
                end
            end
            #if info about columns from boarding info are needed we need to check what boarding_ids fall under the pass_query
            # need to check related data since it depends on different table
            if b_query != ""
                b_ids = db.query("SELECT p.Boarding_ID FROM Passengers p LEFT JOIN Family_On_Board f ON p.Passenger_ID = f.Passenger_ID LEFT JOIN Cabins c ON p.Passenger_ID = c.Passenger_ID WHERE #{pass_query};")
                additional_query = ""
                b_ids.each() do |b_id|
                    if additional_query == ""
                        additional_query = "p.Boarding_ID = #{b_id['Boarding_ID']}"
                    else
                        additional_query = additional_query + " OR p.Boarding_ID = #{b_id['Boarding_ID']}"
                    end
                end
                currentOp = db.query("SELECT #{b_query} FROM Boarding_Info p WHERE #{additional_query};")
                currentOp.each() do |op|
                    op.values.zip(b_column_list).each() do |val, col|
                        puts "<h2> The #{cgi['operation']} of #{col} Where #{pass_query} is #{val.round(2)}"
                    end
                end
            end
        #conditional only apart of boarding info tables
        elsif pass_query == "" && board_query != ""
            if b_query != ""
                currentOp = db.query("SELECT #{b_query} FROM Boarding_Info p WHERE #{board_query};")
                currentOp.each() do |op|
                    op.values.zip(b_column_list).each() do |val, col|
                        puts "<h2> The #{cgi['operation']} of #{col} Where #{pass_query} is #{val.round(2)}"
                    end
                end
            end
            # if info needed about passenger we need to check what boarding ids fit the position
            if p_query != ""
                b_ids = db.query("SELECT Boarding_ID FROM Boarding_Info p WHERE #{board_query};")
                additional_query = ""
                b_ids.each() do |b_id|
                    if additional_query == ""
                        additional_query = "p.Boarding_ID = #{b_id['Boarding_ID']}"
                    else
                        additional_query = additional_query + " OR p.Boarding_ID = #{b_id['Boarding_ID']}"
                    end
                end
                currentOp = db.query("SELECT #{p_query} FROM Passengers p LEFT JOIN Family_On_Board f ON p.Passenger_ID = f.Passenger_ID LEFT JOIN Cabins c ON p.Passenger_ID = c.Passenger_ID WHERE #{additional_query};")
                currentOp.each() do |op|
                    op.values.zip(p_column_list).each() do |val, col|
                        puts "<h2> The #{cgi['operation']} of #{col} Where #{pass_query} is #{val.round(2)}"
                    end
                end
            end
        #conditional for both tables
        elsif pass_query != "" && board_query != ""
            if p_query != ""
                b_ids = db.query("SELECT Boarding_ID FROM Boarding_Info p WHERE #{board_query};")
                additional_query = ""
                b_ids.each() do |b_id|
                    if additional_query == ""
                        additional_query = "p.Boarding_ID = #{b_id['Boarding_ID']}"
                    else
                        additional_query = additional_query + " OR p.Boarding_ID = #{b_id['Boarding_ID']}"
                    end
                end
                currentOp = db.query("SELECT #{p_query} FROM Passengers p LEFT JOIN Family_On_Board f ON p.Passenger_ID = f.Passenger_ID LEFT JOIN Cabins c ON p.Passenger_ID = c.Passenger_ID WHERE #{pass_query} #{cgi['connector']}(#{additional_query});")
                currentOp.each() do |op|
                    op.values.zip(p_column_list).each() do |val, col|
                        puts "<h2> The #{cgi['operation']} of #{col} Where #{pass_query} #{cgi['connector']} #{board_query} is #{val.round(2)}"
                    end
                end
            end

            if b_query != ""
                b_ids = db.query("SELECT p.Boarding_ID FROM Passengers p LEFT JOIN Family_On_Board f ON p.Passenger_ID = f.Passenger_ID LEFT JOIN Cabins c ON p.Passenger_ID = c.Passenger_ID WHERE #{pass_query};")
                additional_query = ""
                b_ids.each() do |b_id|
                    if additional_query == ""
                        additional_query = "b.Boarding_ID = #{b_id['Boarding_ID']}"
                    else
                        additional_query = additional_query + " OR b.Boarding_ID = #{b_id['Boarding_ID']}"
                    end
                end
                currentOp = db.query("SELECT #{b_query} FROM Boarding_Info p WHERE #{b_query} #{cgi['connector']} (#{additional_query});")
                currentOp.each() do |op|
                    op.values.zip(b_column_list).each() do |val, col|
                        puts "<h2> The #{cgi['operation']} of #{col} Where #{pass_query} #{cgi['connector']} #{board_query} is #{val.round(2)}"
                    end
                end
            end
        else
            #ensure all other cases happen
        end
    rescue => e
        #puts e.message
        puts "<meta http-equiv='refresh' content='3;url=calculations.cgi'>"
        puts "<title>ERROR</title></head>"
        puts "<body>"
        puts "<h2>ERROR: There was an issue with the query, check conditionals</h2>"
    end
    puts "</form>"
    puts "</div>"
else
    puts "<title>Calculate</title>"
    puts "</head>"
    puts "<body>"
    puts "<header class='header'>"
    puts "<h1>Make a Calculation</h1>"
    puts "</header>"
    puts "<div class='content3'>"
    puts "<form method='post' action='calculations.cgi'>"

    puts "<legend>Please check the operation you would like to make: </legend><br>"
    puts "<input type='radio' name='operation' value='COUNT' checked> Count(Number of Rows)<br>"
    puts "<input type='radio' name='operation' value='SUM'> Total(Sum)<br>"
    puts "<input type='radio' name='operation' value='AVG'> Average<br>"
   
    puts "<br><legend>Please check all of the columns you would like to see in your Query </legend>"
    puts "<h5> One Operation can be made at a time <br> Count Operation can be applied to either Passenger_ID or Boarding_ID<br> All other attributes could produce false results <br> Total #{cgi['connector']} Average can be applied to multiple attributes with the type Integer #{cgi['connector']} Boolean<br>Integers(I) <br> Boolean(B)</h5>"
    puts "<input type='checkbox' name='p_id' value= 'p.Passenger_ID' > Passenger_ID(I) <br>"
    puts "<input type='checkbox' name='surv' value= 'p.Survive' > Survive(B) <br>"
    puts "<input type='checkbox' name='a' value= 'p.Age' > Age(I) <br>"
    puts "<input type='checkbox' name='sos' value= 'f.Siblings_Or_Spouses' > Siblings/Spouses On Board(I) <br>"
    puts "<input type='checkbox' name='pok' value= 'f.Parents_Or_Kids' > Parents/Kids On Board(I) <br>"
    puts "<input type='checkbox' name='b_id' value= 'p.Boarding_ID' > Boarding_ID(I) <br>"
    puts "<input type='checkbox' name='tNum' value= 'p.Ticket_Number' > Ticket_Number(I) <br>"
    puts "<input type='checkbox' name='cls' value= 'p.Class' > Class(I) <br>"
    puts "<input type='checkbox' name='fre' value= 'p.Fare' > Fare(I) <br><br>"

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
    puts "<input type='radio' id='connector' name='connector' value=' OR '  > OR <br>"
    puts "<input type='hidden' id='submitted' name='submitted' value='true'>"
    puts "<br><input type='submit' value='Submit'>"
    puts "</form>"
    puts "</div>"
end
puts "</body>"
puts "</html>"