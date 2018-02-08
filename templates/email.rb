require 'google/apis/gmail_v1'
require 'mail'
require 'email'
# require 'google/api_client/client_secrets'
module Email
  # Gmail = Google::Apis::GmailV1 # Alias the module
  # service = Gmail::GmailService.new
  def ProviderBounced(service)
    bounced_numbers=[]
    trashed_messages=[]
    # Initialize client with authorization
    # service.authorization = user.access_token
    # have to remove later
    label_id = service.list_user_labels("me").to_h[:labels].find{|label|label[:name]==="bounced"}[:id]
    #Gets array with Message Ids only, filters from bounced label only and not sent
    messages_list = service.list_user_messages("me",{include_spam_trash:true,label_ids:[label_id,:"INBOX"]}).to_h[:messages].map{|message|message[:id]}
    puts(messages_list)
    messages_list.each{|message|
      match = service.get_user_message("me",message)
        if !match.label_ids.include?("SENT")
          results = match.payload.headers.find{|el|
            if (el.name ==="To") && el.value != user.email
              bounced_numbers << el.value
            elsif (el.name==="X-Failed-Recipients")
              bounced_numbers <<el.value
            else
              nil
            end
          }
          !results ? bounced_numbers << match.payload.parts.to_json.scan(/To:([^>]*) \\r/).last.first.strip : nil
          trashed_messages << service.trash_user_message('me',message).id
        end
    }
    {bounced:bounced_numbers,trashed:trashed_messages}
  end

  def Add_phone_number(service,providers={},number,message)
      # providers={
      #   "alltel":	"@text.wireless.alltel.com",
      #   "att&t":	"@txt.att.net",
      #   "boostmobile":	"@myboostmobile.com",
      #   "cricket":	"@sms.mycricket.com",
      #   "sprint":	"@messaging.sprintpcs.com",
      #   "tmobile":	"@tmomail.net",
      #   "uscellular":	"@email.uscc.net",
      #   "verizon":	"@vtext.com",
      #   "virginmobile":	"@vmobl.com"
      # }
      providers={
        "att&t":	"@txt.att.net",
        "tmobile":	"@tmomail.net",
        "uscellular":	"@email.uscc.net",
        "verizon":	"@vtext.com"
      }
      # mail = Mail.new do
      # message_id '<ThisIsMyMessageId@some.domain.com>'
      # from     'me@test.lindsaar.net'
      # to       'you@test.lindsaar.net'
      # subject  'Here is the image you wanted'
      # body     File.read('body.txt')
      # add_file :filename => 'somefile.png', :content => File.read('/somefile.png')
    # end
      message_object = Google::Apis::GmailV1::Message.new
      mail = Mail.new
      mail["from"]="smscampaignmanager@gmail.com"
      providers.each{|name,gateway|
        mail["to"]=number + gateway
        mail['body']=message
        message_object.raw = mail.to_s
        service.send_user_message("me", message_object)
      }

    end

      def Send_campaign(service,providers={
        "att&t":	"@txt.att.net",
        "tmobile":	"@tmomail.net",
        "uscellular":	"@email.uscc.net",
        "verizon":	"@vtext.com",
        "sprint":	"@messaging.sprintpcs.com"
      },number,message,interest)
        mail = Mail.new
        mail["from"]="smscampaignmanager@gmail.com"
        providers.each{|name,gateway|
        mail["to"]=number.gsub(/[^0-9]/, '') + gateway
        mail['body']=message + "I hope you like it ..." + interest
        message_object.raw = mail.to_s
        service.send_user_message("me", message_object)
      }
    end


  end
