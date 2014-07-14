class MessagesController < ApplicationController


  # GET /messages
  # GET /messages.json
  def index
    @messages = Message.all
    @channel = @messages.first.try(:channel).to_s
    

  end

  
end
