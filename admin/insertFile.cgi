#!/usr/bin/ruby

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

db = Mysql2::Client.new(:host=>'10.20.3.4',:username=> 'dbms_cg',:password => 'cg_27_levan', :database=> 'dbms_cg_dbA')

if cgi['uploaded'] != 'true'
    puts "<title>Insert a File</title></head>"
    puts "<body>"
    puts "<header class='header'>"
    puts "<h1>Please Select a File to Upload</h1>"
    puts "</header>"
    puts "<div class='content'>"
    puts "<form id='tags' name='dataEntryTags' enctype='multipart/form-data' action='insertFile.cgi' method='post'>"
    puts "Select file to upload:"
    puts "<input type='file' name='fileName' size='20'>"
    puts "<h2>CSV must be in the following form: <h2>"
    puts "<h4>Survive | Class | Honorific | First Name | Last Name | Unmarried Name | Gender | Age | Siblings/Spouses On Board | Parents/Kids On Board | Ticket Number | Fare | Cabins | Embarked From<h4>"
    puts "<input type='hidden' id='uploaded' name='uploaded' value='true'>"
    puts "<input type='submit'>"
    puts "</form>"
    puts "</div>"
else
    begin
        # create a Tempfile reference
        fromfile = cgi.params['fileName'].first
        originalName = cgi.params['fileName'].first.instance_variable_get("@original_filename")

        # create output file reference as original filename in our chosen directory
        uploadLocation = "/NFSHome/cgartner/public_html/Final/DownloadedFiles/"
        tofile = uploadLocation + originalName

        #check that the file is able to be opened
        File.open(tofile.untaint, 'w') { |file| file << fromfile.read}

        #TABLE SET UPS AND COORDINATION WITH ARRAYS
        #Passengers(Passenger_ID(PK, AUTO_INC), Survive, Honorific, First_Name, Last_Name, Unmarried_Name, Gender, Age, Boarding_ID(FK))
        #Family_On_Board(Passenger_ID(FK), Sibling_Spouses, Parents_Kids)
        #Boarding_Info(Boarding_ID(PK), Class, Ticket_Number, Fare, Embarked_From)
        #Cabins(Passenger_ID(PK,FK), Cabin(PK))
        SURVIVE = 0
        CLASS = 1
        HONORIFIC = 2
        FIRST_NAME = 3
        LAST_NAME = 4
        UNMARRIED_NAME = 5
        GENDER = 6
        AGE = 7
        SIBLING_SPOUSES = 8
        PARENTS_KIDS = 9
        TICKET_NUMBER = 10
        FARE = 11
        CABINS = 12
        EMBARKED_FROM = 13

        lines = IO.readlines(tofile)
        headerPassed = false
        lines.each() do |line|
            # String Build for insertion
            passengers = ""
            family_on_board = ""
            boarding_info = ""
            cabins = ""
            p_id_query = ""
            b_id_query = ""

            unclean_data = line.split("|")
            clean_data = []

            unclean_data.each() do |data|
                stripped_data = data.strip()
                clean_data.push(stripped_data)
            end
            if headerPassed
                #go through each data piece seperately since they each differ in what can be inserted
                if clean_data[SURVIVE] == "True"
                    passengers = "TRUE,"
                    p_id_query = "Survive = 1 AND "
                elsif clean_data[SURVIVE] == "False"
                    passengers = "FALSE,"
                    p_id_query = "Survive = 0 AND "
                else
                    passengers = "NULL,"
                    clean_data[SURVIVE] = "NULL"
                    p_id_query = "Survive IS NULL AND "

                end
                if clean_data[CLASS] != ""
                    boarding_info = "#{clean_data[CLASS]},"
                    b_id_query = "Class = #{clean_data[CLASS]} AND "
                else
                    boarding_info = "NULL,"
                    clean_data[CLASS] = "NULL"
                    b_id_query = "Class IS NULL AND "

                end
                if clean_data[HONORIFIC] != ""
                    passengers = passengers + "'#{clean_data[HONORIFIC]}',"
                    p_id_query = p_id_query + "Honorific = '#{clean_data[HONORIFIC]}' AND "
                else
                    passengers = passengers + "NULL,"
                    clean_data[HONORIFIC] = "NULL"
                    p_id_query = p_id_query + "Honorific IS NULL AND "
                end
                if clean_data[FIRST_NAME] != ""
                    passengers = passengers + "\"#{clean_data[FIRST_NAME]}\","
                    p_id_query = p_id_query + "First_Name = \"#{clean_data[FIRST_NAME]}\" AND "
                else
                    passengers = passengers + "NULL,"
                    clean_data[FIRST_NAME] = "NULL"
                    p_id_query = p_id_query + "First_Name IS NULL AND "
                end
                if clean_data[LAST_NAME] != ""
                    passengers = passengers + "\"#{clean_data[LAST_NAME]}\","
                    p_id_query = p_id_query + "Last_Name = \"#{clean_data[LAST_NAME]}\" AND "
                else
                    passengers = passengers + "NULL,"
                    clean_data[LAST_NAME] = "NULL"
                    p_id_query = p_id_query + "Last_Name IS NULL AND "
                end
                if clean_data[UNMARRIED_NAME] != ""
                    passengers = passengers + "\"#{clean_data[UNMARRIED_NAME]}\","
                    p_id_query = p_id_query + "Unmarried_Name = \"#{clean_data[UNMARRIED_NAME]}\" AND "
                else
                    passengers = passengers + "NULL,"
                    clean_data[UNMARRIED_NAME] = "NULL"
                    p_id_query = p_id_query + "Unmarried_Name IS NULL AND "
                end
                if clean_data[GENDER] != ""
                    passengers = passengers + "'#{clean_data[GENDER]}',"
                    p_id_query = p_id_query + "Gender = '#{clean_data[GENDER]}' AND "
                else
                    passengers = passengers + "NULL,"
                    clean_data[GENDER] = "NULL"
                    p_id_query = p_id_query + "Gender IS NULL AND "
                end
                if clean_data[AGE] != ""
                    passengers = passengers + "'#{clean_data[AGE]}',"
                    p_id_query = p_id_query + "Age = #{clean_data[AGE]} AND "
                else
                    passengers = passengers + "NULL,"
                    clean_data[AGE] = "NULL"
                    p_id_query = p_id_query + "Age IS NULL AND "
                end
                if clean_data[SIBLING_SPOUSES] != ""
                    family_on_board = "#{clean_data[SIBLING_SPOUSES]},"
                else
                    family_on_board = "NULL,"
                    clean_data[SIBLING_SPOUSES] = "NULL"
                end
                if clean_data[PARENTS_KIDS] != ""
                    family_on_board = family_on_board + "#{clean_data[PARENTS_KIDS]}"
                else
                    family_on_boardn = family_on_board + "NULL"
                    clean_data[PARENTS_KIDS] = "NULL"
                end
                if clean_data[TICKET_NUMBER] != ""
                    boarding_info = boarding_info + "#{clean_data[TICKET_NUMBER]},"
                    b_id_query = b_id_query + "Ticket_Number = #{clean_data[TICKET_NUMBER]} AND "
                else
                    boarding_info = boarding_info + "NULL,"
                    clean_data[TICKET_NUMBER] = "NULL"
                    b_id_query = b_id_query + "Ticket_Number IS NULL AND "
                end
                if clean_data[FARE] != ""
                    boarding_info = boarding_info + "#{clean_data[FARE]},"
                    b_id_query = b_id_query + "Fare = #{clean_data[FARE]} AND "
                else
                    boarding_info = boarding_info + "NULL,"
                    clean_data[FARE] = "NULL"
                    b_id_query = b_id_query + "Fare IS NULL AND "
                end
                if clean_data[EMBARKED_FROM] != ""
                    boarding_info = boarding_info + "\"#{clean_data[EMBARKED_FROM]}\""
                    b_id_query = b_id_query + "Embarked_From = \"#{clean_data[EMBARKED_FROM]}\""
                else
                    boarding_info = boarding_info + "NULL"
                    clean_data[EMBARKED_FROM] = "NULL"
                    b_id_query = b_id_query + "Embarked_From IS NULL"
                end

                boarding_id = db.query("SELECT Boarding_ID FROM Boarding_Info WHERE #{b_id_query};")
                if boarding_id.count() == 0
                    #if there wasn't already an id with same information we create one
                    db.query("INSERT INTO Boarding_Info(Class,Ticket_Number,Fare,Embarked_From) VALUES(#{boarding_info});")
                end
                #redo query in case id wasn't inserted yet
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

                if clean_data[CABINS] != ""
                    cabins = clean_data[CABINS].split()
                    cabins.each() do |cabin|
                        db.query("INSERT INTO Cabins VALUES(#{p_id}, '#{cabin}')")
                    end
                else
                    #is null not inserted
                end
            else
                headerPassed = true
            end
        end
        puts "<meta http-equiv='refresh' content='0;url=viewAll.cgi'>"
        puts "</head>"
        puts "<body>"
    rescue
        puts "<meta http-equiv='refresh' content='3;url=insertFile.cgi'>"
        puts "<title>ERROR</title></head>"
        puts "<body>"
        puts "<h2>ERROR: Check File Format</h2>"
    end
end
puts "</body>"
puts "</html>"