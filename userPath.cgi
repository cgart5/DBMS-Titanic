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
puts "<link rel='icon' type='image/x-icon' href='tbat.webp'>"

if cgi['decision'] == 'Admin'
    puts "<meta http-equiv='refresh' content='0;url=admin/admin.cgi'>"
else
    puts "<meta http-equiv='refresh' content='0;url=basicUser/basicUser.cgi'>"   
end
puts "</head>"
puts "</html>" 
