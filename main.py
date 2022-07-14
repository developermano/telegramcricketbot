import logging

from telegram import Bot,InlineKeyboardButton, InlineKeyboardMarkup, ReplyMarkup, Update, ReplyKeyboardMarkup, KeyboardButton, keyboardbutton, user
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from db import tiny

from stats import playerstat

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)



token = "5518535759:AAEG4pTKpkgomCNpoB6GYK6NrWt6Hn8s4A8"
bot=Bot(token)
admin_id=2039990859


def start(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id==admin_id:
        msg='''
    /create - creating a post
        '''
        update.message.reply_text(msg)



def create(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id==admin_id:
        keyboard=[[KeyboardButton("T20"),KeyboardButton("ODI"),KeyboardButton("TEST")]]
        reply_markup=ReplyKeyboardMarkup(keyboard,True)
        update.message.reply_text("send match type:",reply_markup=reply_markup)
        tiny.set_user(update.message.from_user.id,"reqdesc")


def text(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id==admin_id:
        if tiny.get_user_state(update.message.from_user.id)=="reqdesc":
            tiny.set_user("type_"+str(update.message.from_user.id),update.message.text)
            tiny.set_user(update.message.from_user.id,"reqsquad")
            update.message.reply_text("send squad")
            return
        
        if tiny.get_user_state(update.message.from_user.id)=="reqsquad":
            players=str(update.message.text).split(",")
            format=tiny.get_user_state("type_"+str(update.message.from_user.id))
            for player in players:
                ps=playerstat(player,format)
                if ps !="":
                    msg='''
    playername : {}
    country    : {}
    role       : {}
    matches    : {}

    batting:
    runs       : {}
    best score : {}
    average    : {}
    strikerate : {}
    100        : {}
    50         : {}

    bowling :
    balls      : {}
    runs       : {}
    wickets    : {}
    best       : {}
    average    : {}
    5wickets   : {}
                    '''
                    finalmsg=msg.format(ps[0],ps[1],ps[3],ps[4],ps[5],ps[6],ps[7],ps[8],ps[9],ps[10],ps[11],ps[12],ps[13],ps[14],ps[15],ps[16])
                    if update.message.from_user.id==admin_id:
                        if update.message.chat_id==admin_id:
                            bot.send_message("@freecricketstats",finalmsg)
                        else:
                            update.message.reply_text(finalmsg)
            return
    
    msg=update.message.text
    try:
        matchname=msg[msg.index("private contest for the ")+24:msg.index("Spots: ")].rstrip()
        entry=msg[msg.index("Entry: ")+7:msg.index("Spots: ")].rstrip()
        spots=msg[msg.index("Spots: ")+7:msg.index("1st Prize: ")].rstrip()
        istprize=msg[msg.index("1st Prize: ")+11:msg.index("Deadline: ")].rstrip()
        link=msg[msg.index("-Tap ")+5:msg.index("-Use contest code")].rstrip()
        mymsg='''
matchname : {}
entry fee : {}
spots     : {}
1st prize : {}
        '''
        print(msg)
        mymsgfinal=mymsg.format(matchname,entry,spots,istprize)
        keyboard=[[InlineKeyboardButton("join contest",url=link)]]
        reply_markup=InlineKeyboardMarkup(keyboard)
        update.message.reply_text(mymsgfinal,reply_markup=reply_markup)
        update.message.delete()
    except:
        update.message.delete()


def main() -> None:
    """Run the bot."""
    updater = Updater(token)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('create', create))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.text & ~ Filters.command,text))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()