#!/home/ryomatsu/.rbenv/shims/ruby
#
#!/usr/bin/env ruby
# -*- ruby -*-
#
# $Date$
# $Rev$
#
require 'cgi'
require 'digest/md5'
require 'sdbm'
require 'RMagick'

cgi = CGI.new("html3")

id = cgi.params['id'][0].read
imagedata = cgi.params['imagedata'][0].read
hash = Digest::MD5.hexdigest(imagedata)

create_newid = false
if not id or id == "" then
    id = Digest::MD5.hexdigest(cgi.remote_addr + Time.now.to_s)
    create_newid = true
end

dbm = SDBM.open('db/id',0644)
dbm[hash] = id
dbm.close

filename = "img/#{hash}.png"
File.open(filename,"w").print(imagedata)

if imagedata.bytesize > 100000
    image = Magick::Image.from_blob(imagedata).first
    filename = "img/#{hash}.jpeg"
    image.write(filename)
end

headers = {}
if create_newid then
    headers = {"X-Gyazo-Id"=>id}
end

cgi.out(headers){"http://gyazo.loumo.jp/#{filename}"}
