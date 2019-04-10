# coding: utf-8
import datetime
import re
from config import image_sizes
from sqlalchemy import text
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from main import app
from main import database as d


Base = d.Model

'''
Achievement of an athlete. It is not applicable for non-athlete profiles.
used by: athlete
'''
class Achievement(Base):
    __tablename__ = 'achievement'

    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'SET NULL', onupdate=u'CASCADE'))
    title = d.Column(d.String(255))
    summary = d.Column(d.Text)
    year = d.Column(d.Integer)
    icon = d.Column(d.String(255))
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship(u'User')


'''
Always associated with a listing. An athlete can apply for a open listing.
used by: athlete
'''
class Application(Base):
    __tablename__ = 'application'

    id = d.Column(d.Integer, primary_key=True, nullable=False, unique=True)
    listing_id = d.Column(d.ForeignKey(u'listing.id', ondelete=u'CASCADE'), primary_key=True, nullable=False)
    looking_for_id = d.Column(d.ForeignKey(u'looking_for.id', ondelete=u'CASCADE'), nullable=True)
    applicant_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), nullable=False)
    note = d.Column(d.String(500))
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    applicant = relationship(u'User')
    listing = relationship(u'Listing')
    looking_for = relationship(u'LookingFor')

# Regex hyperlinks
hyperlink_regex = re.compile(r'(http|)(s|)(://|)((([-\w]+\.)+([^\s\/]+))([^\s]*)[^,.\s])')


'''
Represents a position and club an athlete played for.
used by: athlete
'''
class CareerItem(Base):
    __tablename__ = 'career_item'

    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'SET NULL', onupdate=u'CASCADE'))
    club_name = d.Column(d.String(30))
    team_name = d.Column(d.String(30))
    location = d.Column(d.String(30))
    level = d.Column(d.String(30))
    date_from = d.Column(d.Date)
    date_till = d.Column(d.Date)
    image = d.Column(d.String(255))
    body = d.Column(d.Text)
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    original_image_name = d.Column(d.String(255))

    # Club this career item is associated with
    club_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'SET NULL', onupdate=u'CASCADE'))

    user = relationship(u'User', primaryjoin=u'CareerItem.user_id == User.id', backref=u'career_items')

    @property
    def body_with_hyperlinks(self):
        return hyperlink_regex.sub(r'<a target="_blank" href="http\2://\4">\1\2\3\5/..</a>', self.body)

    @property
    def image_icon(self):
        if not self.image:
            return ''
        image_url = '/uploads/careerItem/' + self.image
        return image_sizes.get_resized(image_url, 'icon')


'''
The core module that defines relationships for an athlete, agent and club.
Allowed relationship types:
    - current_player:       an athlete is part of the current team: club-athlete
    - past_player:          whether an athlete played with a club in past: club-athlete
    - played_with:          between two athletes - whether they played together somewhere: athlete-athlete
    - current_client:       whether an athlete is a current client for an agent: agent-athlete
    - past_client:          whether an athlete was a client for an agent: agent-athlete
    - want_to_play:         an athlete wants to play in a club: athlete-club
    - want_to_recruit:      a club wants to recruit a given athlete: club-athlete
    - want_to_manage:       an agent want to manage an athlete: agent-athlete
    - want_to_be_managed    an athlete wants to be managed by a club: athlete-agent

used by: athlete, agent & club
'''
class Relate(Base):
    __tablename__ = 'relate'

    id = d.Column(d.BigInteger, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    user_role = d.Column(d.String, index=True) # athlete, agent or club
    athlete_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    type = d.Column(d.String, index=True) # 'current_player', 'past_player', 'played_with', 'current_client', 'past_client', 'want_to_play', 'want_to_recruit', 'want_to_manage', 'want_to_be_managed'

    # This is not yet implemented. the idea is to allow clubs and agents to highlight
    # some of their athletes / clients.
    is_legend = d.Column(d.Boolean, index=True, default=False) # whether athlete is a legend
    year_start = d.Column(d.Integer) # In case of transactional, use this year
    year_end = d.Column(d.Integer)
    athlete_number = d.Column(d.Integer) # Roster Number - not currently used
    approved = d.Column(d.Boolean, default=False) # not currently used
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = d.Column(d.String) # athlete, agent or club
    

    # TODO(ankit): Used when agent specifies which club he recruited player for
    club_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'SET NULL', onupdate=u'CASCADE'), nullable=True)

    # For athlete-athlete relation, specify career_item.
    career_item_id = d.Column(d.ForeignKey(u'career_item.id', ondelete=u'SET NULL', onupdate=u'CASCADE'), nullable=True)

    user = relationship(u'User', primaryjoin=u'Relate.user_id == User.id')
    athlete = relationship(u'User', primaryjoin=u'Relate.athlete_id == User.id')
    career_item = relationship(u'CareerItem', backref=u'career_items', uselist=False)



'''
Deprecated, not used anymore.
'''
class CgGame(Base):
    __tablename__ = 'cg_game'
    __table_args__ = (
        d.Index(u'cg_game_date_index', u'game_date', unique=False),
        d.Index(u'cg_game_number_index', u'number', unique=False),
    )

    id = d.Column(d.Integer, primary_key=True)
    cg_team_id = d.Column(d.ForeignKey(u'cg_team.id', ondelete=u'CASCADE'))
    number = d.Column(d.Integer)
    game_date = d.Column(d.DateTime)
    game_date_status = d.Column(d.Integer)
    opponent = d.Column(d.String(255))
    location = d.Column(d.String(255))

    cg_team = relationship(u'CgTeam')


'''
Deprecated, not used anymore.
'''
class CgLeague(Base):
    __tablename__ = 'cg_league'
    __table_args__ = (
        d.Index(u'cg_league_name_index', u'name', unique=False),
    )
    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'))
    name = d.Column(d.String(255))

    user = relationship(u'User')


'''
Deprecated, not used anymore.
'''
class CgTeam(Base):
    __tablename__ = 'cg_team'
    __table_args__ = (
        d.Index(u'cg_team_name_index', u'name', unique=False),
    )

    id = d.Column(d.Integer, primary_key=True)
    cg_league_id = d.Column(d.ForeignKey(u'cg_league.id', ondelete=u'CASCADE'))
    name = d.Column(d.String(255))

    cg_league = relationship(u'CgLeague')



'''
Represents a client of an agent. This is also not used anymore. We instead now create
a new user-profile for every client. These newly created profiles are called "managed profiles".
They will have the managed_by_id of the agent who manages them.
'''
class Client(Base):
    __tablename__ = 'client'

    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), nullable=False)
    sport_id = d.Column(d.ForeignKey(u'sport.id', ondelete=u'SET NULL'))
    firstname = d.Column(d.String(50))
    lastname = d.Column(d.String(50))
    club_name = d.Column(d.String(100))
    image = d.Column(d.String(255))
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    sport = relationship(u'Sport')
    user = relationship(u'User',
        backref=backref(u'clients', uselist=True, lazy=u'select'))

    @property
    def name(self):
        return self.firstname + ' ' + self.lastname


'''
Deprecated. Not used anymore.
'''
class ClubGame(Base):
    __tablename__ = 'club_game'

    id = d.Column(d.Integer, primary_key=True, nullable=False, unique=True)
    club_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), primary_key=True, nullable=False)
    team = d.Column(d.String(100))
    opponent = d.Column(d.String(100))
    date = d.Column(d.Date)
    time = d.Column(d.Time)
    location = d.Column(d.String(500))
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    autocomplete = d.Column(d.Boolean, default=False)

    club = relationship(u'User')


'''
List of all countries and an ID associated with them.
Country slug just represents the name in lower case.
'''
class Country(Base):
    __tablename__ = 'country'

    id = d.Column(d.Integer, primary_key=True)
    slug = d.Column(d.String(64))
    name = d.Column(d.String(64))


'''
Represents a self-defined endorsement.
used by: athletes
'''
class Endorsement(Base):
    __tablename__ = 'endorsement'

    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'SET NULL', onupdate=u'CASCADE'))
    abbreviation = d.Column(d.Integer)
    first_name = d.Column(d.String(255))
    last_name = d.Column(d.String(255))
    date = d.Column(d.Date)
    title = d.Column(d.String(255))
    body = d.Column(d.Text)
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship(u'User')

    @property
    def abbreviation_str(self):
        if self.abbreviation is None:
            return ''
        return ['Mr', 'Mrs'][self.abbreviation]


'''
If someone likes a post (similar to FB like).
'''
class FavouritePost(Base):
    __tablename__ = 'favourite_post'
    __table_args__ = (
        UniqueConstraint(u'post_id', u'user_id', name=u'uniquecombi'),
    )

    post_id = d.Column(d.ForeignKey(u'post.id', ondelete=u'CASCADE', onupdate=u'CASCADE'))
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE', onupdate=u'CASCADE'))
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    id = d.Column(d.Integer, primary_key=True)

    post = relationship(u'Post')
    user = relationship(u'User')


'''
Deprecated, not used anywhere.
'''
class Lifestyle(Base):
    __tablename__ = 'lifestyle'

    id = d.Column(d.Integer, primary_key=True)
    slug = d.Column(d.String(64))
    name = d.Column(d.String(64))


'''
Deprecated, not used anymore.
'''
class LimitedAccessWhitelistedIp(Base):
    __tablename__ = 'limited_access_whitelisted_ip'

    id = d.Column(d.Integer, primary_key=True)
    ip_address = d.Column(d.String(128))


'''
This is the core module to define an opportunity posted by a club.
status:
    - active: the listing is still accepting applications
    - closed: represents the listing was deleted by the club. In this case,
        closed_reason should be set. If hired on platform, hired_user_id might be set.
        hired_email is set if not hired on platform.
used by: club
'''
class Listing(Base):
    __tablename__ = 'listing'

    id = d.Column(d.Integer, primary_key=True, nullable=False, unique=True)
    status = d.Column(d.String, default='active') # option: active, closed
    club_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), primary_key=True, nullable=False)
    position_id = d.Column(d.ForeignKey(u'position.id', ondelete=u'CASCADE'), primary_key=True, nullable=False)
    division = d.Column(d.String(50))
    headline = d.Column(d.String(200))
    description = d.Column(d.String(1000))
    season_start = d.Column(d.Date)
    closed_reason = d.Column(d.String) # found_on_sporple, found_elsewhere, no_hire
    hired_user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'SET NULL'))
    hired_email = d.Column(d.String)
    sport_id = d.Column(d.ForeignKey(u'sport.id', ondelete=u'SET NULL'), nullable=True)

    # Premium features
    height_min = d.Column(d.Integer, default=0)
    height_max = d.Column(d.Integer, default=999)
    weight_min = d.Column(d.Integer, default=0)
    weight_max = d.Column(d.Integer, default=999)
    age_min = d.Column(d.Integer, default=0)
    age_max = d.Column(d.Integer, default=99)

    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    club = relationship(u'User', uselist=False, primaryjoin=u'Listing.club_id == User.id',
        backref=backref(u'listings', uselist=True, lazy=u'select'))
    position = relationship(u'Position')
    country_groups = relationship(u'CountryGroup', secondary='country_group_listing')

'''
Similar to Listing but this is created by agents. Athletes cannot
apply to LookingFor but agents can open and close the looking for as they like.
'''
class LookingFor(Base):
    __tablename__ = 'looking_for'

    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), nullable=False)
    sport_id = d.Column(d.ForeignKey(u'sport.id', ondelete=u'SET NULL'))
    country_id = d.Column(d.ForeignKey(u'country.id'))
    title = d.Column(d.String(255)) # deprecated
    body = d.Column(d.Text)
    position_id = d.Column(d.ForeignKey(u'position.id', ondelete=u'SET NULL'))

    # Premium features
    height_min = d.Column(d.Integer, default=0)
    height_max = d.Column(d.Integer, default=999)
    weight_min = d.Column(d.Integer, default=0)
    weight_max = d.Column(d.Integer, default=999)
    age_min = d.Column(d.Integer, default=0)
    age_max = d.Column(d.Integer, default=99)

    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    country = relationship(u'Country')
    sport = relationship(u'Sport')
    user = relationship(u'User',
        backref=backref(u'looking_for_list', uselist=True, lazy=u'select'))
    position = relationship(u'Position')
    country_groups = relationship(u'CountryGroup', secondary=u'country_group_looking_for')


'''
Represents all marital statuses:
    1 - single
    2 - married
    3 - engaged
    4 - relationship
    5 - private
'''
class MaritalStatus(Base):
    __tablename__ = 'marital_status'

    id = d.Column(d.Integer, primary_key=True)
    slug = d.Column(d.String(64))
    name = d.Column(d.String(64))


'''
Represents each individual message sent between two users.
Each message is associated with a MessageThread. When a message is sent,
if it's a message between two users who have never talked before, we
create a MessageThread and two MessageThreadUser. The primary purpose of
MessageThreadUser is to track the number of unread messsages in a thread
for that specific user. user_id in this module represents the sender of message.

Each message can also contain up to 1 attachment. This attachment is stored
on S3, with the path to the file in attachment attribute.

This model can potentially support conversation of more than two users, but
is not implemented right now.
'''
class Message(Base):
    __tablename__ = 'message'
    __table_args__ = (
        d.Index(u'message_thread_id_idx', u'thread_id', unique=False),
    )

    id = d.Column(d.Integer, primary_key=True)
    message_type = d.Column(d.Integer, server_default=text("'1'"))
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), nullable=False)
    thread_id = d.Column(d.ForeignKey(u'message_thread.id', ondelete=u'CASCADE'), nullable=False)
    body = d.Column(d.Text)
    attachment = d.Column(d.String(255))
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    thread = relationship(u'MessageThread')
    user = relationship(u'User')

    @property
    def has_image(self):
        if self.attachment:
            for ext in ['jpg', 'png', 'jpeg', 'gif']:
                if self.attachment.endswith(ext):
                    return True
        return False


'''
Represents the conversation between users. Each MessageThread also creates
MessageThreadUser that represents individual user related information for each
thread. latest_message_body is used to show a sneak peek preview of the entire
message on the thread home.
user_ids_string is used to store all the users on the thread comma separated.
user_ids_string is set but not used anymore.
'''
class MessageThread(Base):
    __tablename__ = 'message_thread'
    __table_args__ = (
        d.Index(u'message_thread_nb_thread_users', u'nb_thread_users', unique=False),
        d.Index(u'message_thread_user_ids_string', u'user_ids_string', unique=False),
        d.Index(u'message_thread_user_id_idx', u'user_id', unique=False),
    )

    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), nullable=False)
    latest_message_body = d.Column(d.Text)
    latest_message_user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'SET NULL'))
    latest_message_attachment = d.Column(d.String(255))
    nb_thread_users = d.Column(d.Integer)
    user_ids_string = d.Column(d.String(255))
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    latest_message_user = relationship(u'User', primaryjoin='MessageThread.latest_message_user_id == User.id')
    user = relationship(u'User', primaryjoin='MessageThread.user_id == User.id')

    def get_other_user(self, user_id):
        user_ids = self.user_ids_string.split(',')
        user_ids = [int(id) for id in user_ids if int(id) != user_id]
        # Hack to get the message user.
        if not user_ids:
            message_users = MessageThreadUser.query.filter_by(thread_id=self.id).all()
            for message_user in message_users:
                if message_user.user_id != user_id:
                    return message_user.user
            return None
        return User.query.get(user_ids[0])


'''
Created per MessageThread per user. Stores user specific information
per thread. Primarily used to store number of unread messages by user.
'''
class MessageThreadUser(Base):
    __tablename__ = 'message_thread_user'
    __table_args__ = (
        d.Index(u'message_thread_user_thread_id_idx', u'thread_id', unique=False),
        d.Index(u'message_thread_user_user_id_idx', u'user_id', unique=False),
    )

    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), nullable=False)
    thread_id = d.Column(d.ForeignKey(u'message_thread.id', ondelete=u'CASCADE'), nullable=False)
    nb_unread_messages = d.Column(d.Integer, default=0)
    latest_message_body = d.Column(d.Text)
    other_user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), nullable=True)

    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    thread = relationship(u'MessageThread')
    user = relationship(u'User', primaryjoin='MessageThreadUser.user_id == User.id')
    other_user = relationship(u'User', primaryjoin='MessageThreadUser.other_user_id == User.id', lazy=u'joined')


'''
STATIC: Similar to Country, stores a list of all possible nationalities.
'''
class Nationality(Base):
    __tablename__ = 'nationality'

    id = d.Column(d.Integer, primary_key=True)
    slug = d.Column(d.String(64))
    name = d.Column(d.String(64))
    country_group_id = d.Column(d.ForeignKey(u'country_group.id', ondelete=u'SET NULL'), nullable=True)

    country_group = relationship(u'CountryGroup')


'''
STATIC: Grouping of nationality based on region. This is used in listings.
'''
class CountryGroup(Base):
    __tablename__ = 'country_group'

    id = d.Column(d.Integer, primary_key=True)
    name = d.Column(d.String(100))


t_country_group_listing = d.Table(
    u'country_group_listing',
    d.Column('country_group_id', d.ForeignKey(u'country_group.id', ondelete=u'CASCADE'), primary_key=True, nullable=False),
    d.Column('listing_id', d.ForeignKey(u'listing.id'), primary_key=True, nullable=False),
)


t_country_group_looking_for = d.Table(
    u'country_group_looking_for',
    d.Column('country_group_id', d.ForeignKey(u'country_group.id', ondelete=u'CASCADE'), primary_key=True, nullable=False),
    d.Column('looking_for_id', d.ForeignKey(u'looking_for.id'), primary_key=True, nullable=False),
)


'''
Stores the list of all images uploaded by user in gallery. It also stores
any attachments added in a Post. Value of attachable_model is Post for all
attachments related to Post otherwise is sfGuardUserProfile. All file paths
are for s3 where files are stored.
The tablename ooip_attachment is due to legacy reasons.
'''
class Attachment(Base):
    __tablename__ = 'ooip_attachment'
    __table_args__ = (
        d.Index(u'ooip_attachment_attachments_index', u'attachment_namespace', u'attachable_model', u'attachable_id'),
        d.Index(u'ooip_attachment_object_index', u'attachable_model', u'attachable_id'),
        d.Index(u'ooip_attachment_author_index', u'author_id', unique=False),
    )

    id = d.Column(d.Integer, primary_key=True)
    attachable_model = d.Column(d.String(30))
    attachable_id = d.Column(d.Integer)
    attachment_namespace = d.Column(d.String(50), default='default')
    title = d.Column(d.String(100))
    text = d.Column(d.Text)
    author_id = d.Column(d.Integer)
    author_name = d.Column(d.String(50))
    author_email = d.Column(d.String(100))
    author_website = d.Column(d.String(255))
    folder = d.Column(d.String(255))
    filename = d.Column(d.String(255))
    filename_cropped = d.Column(d.String(255))
    filesize = d.Column(d.Integer)
    filetype = d.Column(d.String(64))
    fileextension = d.Column(d.String(16))
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)

    @property
    def link(self):
        if not self.folder:
            if not self.filename or not self.fileextension:
                return ''
            else:
                return '/uploads/' + self.filename + '.' + self.fileextension
        return '/uploads/' + self.folder + '/' + self.filename + '.' + self.fileextension

    @property
    def thumb_link(self):
        return image_sizes.get_resized(self.link, 'thumb')


'''
STATIC: All possible positions per sport.
'''
class Position(Base):
    __tablename__ = 'position'

    id = d.Column(d.Integer, primary_key=True)
    sport_id = d.Column(d.ForeignKey(u'sport.id', ondelete=u'CASCADE'), nullable=False)
    slug = d.Column(d.String(64))
    name = d.Column(d.String(64))

    sport = relationship(u'Sport', backref=backref(u'positions', uselist=True))
    users = relationship(u'User', secondary='user_position', backref='positions')


'''
Represents a Post done on home page.
A welcome_post is an auto-generated post that is created when a user signs up.
post-share feature is deprecated.
global_* parameters define where the post will be visible. See posts/controller.py for details.
'''
class Post(Base):
    __tablename__ = 'post'

    id = d.Column(d.Integer, primary_key=True)
    body = d.Column(d.Text)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE', onupdate=u'CASCADE'))
    shared_post_id = d.Column(d.ForeignKey(u'post.id', ondelete=u'SET NULL'))
    nb_favourites = d.Column(d.Integer)
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    global_role_id = d.Column(d.ForeignKey(u'role.id', ondelete=u'SET NULL', onupdate=u'CASCADE'))
    global_all_roles = d.Column(d.Boolean, default=False)
    global_all_sports = d.Column(d.Boolean, default=False)
    welcome_post = d.Column(d.Boolean, default=False)

    global_role = relationship(u'Role')
    shared_post = relationship(u'Post', remote_side=[id])
    user = relationship(u'User')
    sports = relationship(u'Sport', secondary='post_sport')

    @property
    def is_by_admin(self):
        if self.welcome_post:
            return False
        if self.global_role_id or self.sports or self.global_all_roles or self.global_all_sports:
            return True
        return False

    def has_favourited(self, user_id):
        # Whether the given user_id has favourited this post.
        return bool(
            FavouritePost.query
                .filter_by(post_id=self.id)
                .filter_by(user_id=user_id)
                .first())

    def get_attachments(self):
        return (Attachment.query
            .filter_by(attachable_model='Post')
            .filter_by(attachable_id=self.id)
            .all())

    def get_comments(self):
        return (Comment.query
            .filter_by(commentable_model='Post')
            .filter_by(commentable_id=self.id)
            .order_by(Comment.created_at.asc())
            .all())


t_post_sport = d.Table(
    'post_sport',
    d.Column('post_id', d.ForeignKey(u'post.id', ondelete=u'CASCADE'), primary_key=True, nullable=False),
    d.Column('sport_id', d.ForeignKey(u'sport.id'), primary_key=True, nullable=False),
)


t_propel_migration = d.Table(
    'propel_migration',
    d.Column('version', d.Integer, default=0)
)


'''
Represents the qualification of an agent. Not verified from anywhere.
used by: agent
'''
class Qualification(Base):
    __tablename__ = 'qualification'

    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'SET NULL', onupdate=u'CASCADE'))
    title = d.Column(d.String(255))
    summary = d.Column(d.Text)
    year = d.Column(d.Integer)
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship(u'User',
        backref=backref(u'qualifications', uselist=True, lazy=u'select'))


'''
RelatedProfileCriterion is a list of criteria to define how related
profiles are calculated. Deprecated now.
'''
class RelatedProfileCriterion(Base):
    __tablename__ = 'related_profile_criteria'

    id = d.Column(d.Integer, primary_key=True)
    name = d.Column(d.String(50))
    target = d.Column(d.String(100))
    is_strict = d.Column(d.Integer, server_default=text("'0'"))
    is_enabled = d.Column(d.Integer, server_default=text("'0'"))


'''
STATIC: Represents all possible roles: agent, club and athlete
'''
class Role(Base):
    __tablename__ = 'role'

    id = d.Column(d.Integer, primary_key=True)
    slug = d.Column(d.String(64))
    name = d.Column(d.String(64))


'''
Deprecated: was orginally used to manage session. Now these are automatically
managed using Flask-Session and Redis.
'''
class Session(Base):
    __tablename__ = 'sessions'
    __table_args__ = (
        d.Index(u'sessions_sess_id', u'sess_id', unique=False),
    )

    sess_id = d.Column(d.String(64), nullable=False)
    sess_data = d.Column(d.Text, nullable=False)
    sess_time = d.Column(d.Integer, nullable=False)
    id = d.Column(d.Integer, primary_key=True)


'''
Deprecated.
'''
class SfCombine(Base):
    __tablename__ = 'sf_combine'

    asset_key = d.Column(d.String(40), primary_key=True)
    files = d.Column(d.String, nullable=False)


'''
Used to store all comments related to post.
'''
class Comment(Base):
    __tablename__ = 'sf_comment'
    __table_args__ = (
        d.Index(u'sf_comment_comments_index', u'comment_namespace', u'commentable_model', u'commentable_id'),
        d.Index(u'sf_comment_object_index', u'commentable_model', u'commentable_id'),
        d.Index(u'sf_comment_author_index', u'author_id', unique=False),
    )

    id = d.Column(d.Integer, primary_key=True)
    commentable_model = d.Column(d.String(30))
    commentable_id = d.Column(d.Integer)
    comment_namespace = d.Column(d.String(50))
    title = d.Column(d.String(100))
    text = d.Column(d.Text)
    author_id = d.Column(d.Integer)
    author_name = d.Column(d.String(50))
    author_email = d.Column(d.String(100))
    author_website = d.Column(d.String(255))
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)

    def get_author(self):
        return User.query.get(self.author_id)


'''
Deprecated.
'''
class SfGuardGroup(Base):
    __tablename__ = 'sf_guard_group'

    id = d.Column(d.Integer, primary_key=True)
    name = d.Column(d.String(255), nullable=False, unique=True)
    description = d.Column(d.Text)

    permissions = relationship(u'SfGuardPermission', secondary='sf_guard_group_permission')
    users = relationship(u'User', secondary='sf_guard_user_group')


t_sf_guard_group_permission = d.Table(
    'sf_guard_group_permission',
    d.Column('group_id', d.ForeignKey(u'sf_guard_group.id', ondelete=u'CASCADE'), primary_key=True, nullable=False),
    d.Column('permission_id', d.ForeignKey(u'sf_guard_permission.id', ondelete=u'CASCADE'), primary_key=True, nullable=False),
)


'''
Deprecated
'''
class SfGuardPermission(Base):
    __tablename__ = 'sf_guard_permission'

    id = d.Column(d.Integer, primary_key=True)
    name = d.Column(d.String(255), nullable=False, unique=True)
    description = d.Column(d.Text)

    users = relationship(u'User', secondary='sf_guard_user_permission')


'''
Deprecated
'''
class SfGuardRememberKey(Base):
    __tablename__ = 'sf_guard_remember_key'

    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), primary_key=True, nullable=False)
    remember_key = d.Column(d.String(32))
    ip_address = d.Column(d.String(50), primary_key=True, nullable=False)
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)

    user = relationship(u'User', uselist=False)


'''
Details related to user-login. Also stores password with added salt.
User and UserProfile objects are tightly coupled and are usually fetched together
due to lazy-joined attribute.
'''
class User(Base):
    __tablename__ = 'sf_guard_user'

    id = d.Column(d.Integer, primary_key=True)
    username = d.Column(d.String(128), nullable=False, unique=True)
    algorithm = d.Column(d.String(128), nullable=False, server_default=text("'sha1'"))
    salt = d.Column(d.String(128), nullable=False)
    password = d.Column(d.String(128), nullable=False)
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    last_login = d.Column(d.DateTime)
    is_active = d.Column(d.Boolean, nullable=False, default=True)
    is_super_admin = d.Column(d.Boolean, nullable=False, default=False)
    unclaimed = d.Column(d.Boolean, default=False)

    profile = relationship(u'UserProfile', primaryjoin=u'UserProfile.user_id == User.id',
            uselist=False, lazy=u'joined', backref=backref(u'user', lazy=u'joined'))
    sports = relationship(u'Sport', secondary='user_sport', uselist=True)

    @property
    def sport(self):
        if self.sports:
            for sport in self.sports:
                if sport.slug == 'rugby':
                    return sport
            return self.sports[0]
        return None

    # Used for legacy reasons.
    # TODO(ankit): Remove list support
    @property
    def sports_list(self):
        return [] if not self.sports else [self.sport]

    @property
    def sport_slug(self):
        return '' if not self.sports else self.sport.slug

    @property
    def sports_string(self):
        return self.sport_slug.capitalize()

    @property
    def role_slug(self):
        return self.profile.role.slug if self.profile and self.profile.role else ''

    @property
    def plan(self):
        return self.profile.plan

    @property
    def name(self):
        if self.profile.role and self.profile.role.slug == 'club':
            return self.profile.club_name or ''
        elif self.profile.firstname and self.profile.lastname:
            return self.profile.firstname + ' ' + self.profile.lastname
        else:
            return self.profile.firstname or ''

    @property
    def slug(self):
        return self.profile.slug

    # Deprecated
    @property
    def test_profile(self):
        return self.id in app.config['TEST_PROFILE_IDS']

    def can_send_message(self):
        return self.plan == 'pro' or self.role_slug == 'athlete'

    def can_upgrade(self):
        return self.plan != 'pro' and self.role_slug != 'athlete'

    def is_premium(self):
        return self.plan == 'pro' and self.role_slug != 'athlete'

    def has_msg_limit_reached(self):
        if self.plan == 'pro':
            return False

        now = datetime.datetime.now()
        yday = now - datetime.timedelta(days=1)
        threads_count = (MessageThreadUser.query
                .filter_by(user_id=self.id)
                .filter(MessageThreadUser.created_at > yday)
                .count())
        return threads_count > 9

    def get_unread_messages(self):
        message_user = MessageUser.query.get(self.id)
        return message_user.nb_unread_messages if message_user else 0

    def get_followers_count(self):
        return UserConnection.query.filter_by(other_user_id=self.id).count()

    def get_following_count(self):
        return UserConnection.query.filter_by(user_id=self.id).count()

    def is_following(self, user_id):
        # If self is following user_id
        return bool(UserConnection.query
                .filter_by(user_id=self.id)
                .filter_by(other_user_id=user_id)
                .first())

    def is_followed_by(self, user_id):
        # If self is followed by user_id
        return bool(UserConnection.query
                .filter_by(user_id=user_id)
                .filter_by(other_user_id=self.id)
                .first())

    def has_applied(self, listing_id, role):
        if role == 'club':
            return bool(Application.query
                    .filter_by(listing_id=listing_id)
                    .filter_by(applicant_id=self.id)
                    .first())
        else:
            return bool(Application.query
                        .filter_by(looking_for_id=listing_id)
                        .filter_by(applicant_id=self.id)
                        .first())
'''
All Non-login related attributes of User. The User-UserProfile objects are
tightly coupled and are fetched together due to lazy-joined property in User.
'''
class UserProfile(Base):
    __tablename__ = 'sf_guard_user_profile'

    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), primary_key=True)
    managed_by_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'SET NULL'))
    # A legend profile cannot be claimed (all legends profile should be unclaimed)
    legend = d.Column(d.Boolean, default=False)
    role_id = d.Column(d.ForeignKey(u'role.id'))
    firstname = d.Column(d.String(50))
    lastname = d.Column(d.String(50))
    birthday = d.Column(d.Date)
    gender = d.Column(d.Integer)
    accepted_terms = d.Column(d.Boolean, default=True)
    lifestyle_id = d.Column(d.ForeignKey(u'lifestyle.id'))
    is_professional = d.Column(d.Boolean, default=False)
    height = d.Column(d.Integer)
    weight = d.Column(d.Integer)
    facebook_uid = d.Column(d.String(128))
    featured = d.Column(d.Boolean)
    club_name = d.Column(d.String(100))
    club_representative_firstname = d.Column(d.String(50))
    club_representative_lastname = d.Column(d.String(50))
    club_representative_email = d.Column(d.String(50))
    club_league = d.Column(d.String(50))
    club_location = d.Column(d.String(255))
    year_establishment = d.Column(d.String(50))
    club_contact_url = d.Column(d.String(255))
    club_contact_email = d.Column(d.String(50))
    school_country_id = d.Column(d.ForeignKey(u'country.id'))
    school_name = d.Column(d.String(50))
    school_zipcode = d.Column(d.String(20))
    school_street = d.Column(d.String(50))
    school_suburb = d.Column(d.String(50))
    college_country_id = d.Column(d.ForeignKey(u'country.id'))
    college_name = d.Column(d.String(50))
    college_zipcode = d.Column(d.String(20))
    college_street = d.Column(d.String(50))
    college_suburb = d.Column(d.String(50))
    occupation = d.Column(d.String(255))
    current_club = d.Column(d.String(100))
    current_team = d.Column(d.String(100))
    current_division = d.Column(d.String(100))
    has_agent = d.Column(d.Integer)
    agent_firstname = d.Column(d.String(50))
    agent_lastname = d.Column(d.String(50))
    agent_email = d.Column(d.String(50))
    agency_name = d.Column(d.String(255))
    agency_url = d.Column(d.String(255))
    agency_image = d.Column(d.String(255))
    years_experience = d.Column(d.Integer)
    image = d.Column(d.String(255))
    nationality_id = d.Column(d.ForeignKey(u'nationality.id'))
    passport_1_id = d.Column(d.ForeignKey(u'nationality.id'))
    passport_2_id = d.Column(d.ForeignKey(u'nationality.id'))
    address_country_id = d.Column(d.ForeignKey(u'country.id'))
    address_zipcode = d.Column(d.String(20))
    address_street = d.Column(d.String(50))
    address_suburb = d.Column(d.String(50))
    address_city = d.Column(d.String(50))
    phonenumber = d.Column(d.String(50))
    marital_status_id = d.Column(d.ForeignKey(u'marital_status.id'))
    children = d.Column(d.Boolean, default=False)
    reel_video_url = d.Column(d.String(255))
    reel_image = d.Column(d.String(255))
    personal_statement = d.Column(d.Text)
    career_summary = d.Column(d.Text)
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    reel_video_url_original = d.Column(d.String(255))
    twitter_account = d.Column(d.String(255))
    slug = d.Column(d.String(255))
    needs_password_reset = d.Column(d.Boolean, default=False)
    password_setup = d.Column(d.Boolean, default=True)
    reel_video_type = d.Column(d.String(50))
    midnight_madness = d.Column(d.Boolean, default=False)
    is_reviewed = d.Column(d.Boolean, default=False)
    device = d.Column(d.String(200))
    plan = d.Column(d.String, default='intro')

    address_country = relationship(u'Country', primaryjoin='UserProfile.address_country_id == Country.id')
    college_country = relationship(u'Country', primaryjoin='UserProfile.college_country_id == Country.id')
    lifestyle = relationship(u'Lifestyle')
    marital_status = relationship(u'MaritalStatus')
    nationality = relationship(u'Nationality', primaryjoin='UserProfile.nationality_id == Nationality.id')
    passport_1 = relationship(u'Nationality', primaryjoin='UserProfile.passport_1_id == Nationality.id')
    passport_2 = relationship(u'Nationality', primaryjoin='UserProfile.passport_2_id == Nationality.id')
    role = relationship(u'Role')
    school_country = relationship(u'Country', primaryjoin='UserProfile.school_country_id == Country.id')
    managed_by = relationship(u'User', primaryjoin='UserProfile.managed_by_id == User.id')

    @property
    def fullname(self):
        if self.firstname and self.lastname:
            return self.firstname + ' ' + self.lastname
        else:
            return self.firstname or ''

    @property
    def age(self):
        born = self.birthday
        if not born:
            return None
        today = datetime.date.today()
        return (today.year - born.year
            - ((today.month, today.day) < (born.month, born.day)))

    @property
    def sport(self):
        return self.user.sport

    @property
    def address_country_slug(self):
        if self.address_country:
            return self.address_country.name
        else:
            return ''

    @property
    def nationality_slug(self):
        if self.nationality:
            return self.nationality.name
        else:
            return ''

    @property
    def is_owner(self, user_id):
        return self.user_id == user_id or self.managed_by_id == user_id

    @property
    def passports_slug(self):
        passports = ''
        if self.passport_1:
            passports = self.passport_1.name
        if self.passport_2:
            passports += (', ' if passports else '') + self.passport_2.name
        return passports

    @property
    def gender_slug(self):
        if self.gender == 0:
            return 'male'
        elif self.gender == 1:
            return 'female'
        return ''

    @property
    def positions_string(self):
        if not self.user.positions:
            return ''
        positions = [p.name for p in self.user.positions]
        return ','.join(positions)

    @property
    def first_position(self):
        return self.user.positions[0] if self.user.positions else ''

    @property
    def first_position_string(self):
        position = self.first_position
        return position.name if position else ''

    @property
    def agency_url_link(self):
        # Add http if the site doesn't begin with http
        if self.agency_url and not self.agency_url.startswith('http'):
            return 'http://' + self.agency_url
        return self.agency_url

    @property
    def agency_url_name(self):
        # Remove http if present.
        if self.agency_url and self.agency_url.startswith('http'):
            return self.agency_url  \
                .replace('http://', '') \
                .replace('https://', '')
        return self.agency_url

    @property
    def club_url_link(self):
        # Add http if the site doesn't begin with http
        if self.club_contact_url and not self.club_contact_url.startswith('http'):
            return 'http://' + self.club_contact_url
        return self.club_contact_url


    @property
    def club_url_name(self):
        # Remove http if present.
        if self.club_contact_url and self.club_contact_url.startswith('http'):
            return self.club_contact_url \
                .replace('http://', '')  \
                .replace('https://', '')

    @property
    def reel_url(self):
        reel_image_url = self.reel_image
        if not reel_image_url and self.user.sport_slug != 'baseball':
            reel_image_url = '/static/images/profile/default-' + self.user.sport_slug + '.jpg'
        return reel_image_url

    @property
    def years_experience_string(self):
        if self.years_experience and self.years_experience > 9:
            return '10+'
        else:
            return 'unknown'

    @property
    def full_address(self):
        address = ''
        if self.address_street:
            address = self.address_street
        if self.address_suburb:
            if not address:
                address = self.address_suburb
            else:
                address += ', ' + self.address_suburb
        if self.address_city:
            if not address:
                address = self.address_city
            else:
                address += ', ' + self.address_city
        if self.address_country:
            if not address:
                address = self.address_country.slug
            else:
                address += ', ' + self.address_country.slug
        if self.address_zipcode:
            if not address:
                address = self.address_zipcode
            else:
                address += ' - ' + self.address_zipcode
        return address

    @property
    def is_allowed_to_message(self):
        from profile import controller as pcontroller
        listings = pcontroller.get_listings(self)
        if listings:
            is_allowed = map(pcontroller.is_user_eligible, listings)
            return any(is_allowed)
        else:
            return True

    def get_followers_count(self):
        return self.user.get_followers_count()

    '''
    Get image url based on size. Available sizes:
        standard:   200x200
        large:      400x400
        small:      102x102
        x-small:    60x60
    '''
    def get_image(self, size='standard', default=True):
        if (not self.image or not self.image.strip()) and default:
            if self.role and self.role.slug == 'club':
                return '/static/images/profile/Clubs-default.png'

            return '/static/images/profile/empty_profile_image.png'

        image_url = '/uploads/profile/' + self.image.strip()
        if size != 'standard':
            image_url = image_sizes.get_resized(image_url, size)
        return image_url

    '''
    Support images sizes: small and standard.
    '''
    def get_agency_image(self, size='small'):
        if not self.agency_image or not self.agency_image.strip():
            return ''
        image_url = '/uploads/profile/' + self.agency_image.strip()
        if size != 'standard':
            image_url = image_sizes.get_resized(image_url, size)
        return image_url


    def get_attachments(self):
        return (Attachment.query
                .filter_by(attachable_model='sfGuardUserProfile')
                .filter_by(attachable_id=self.user_id)
                .all())


'''
This represents total number of unread message threads by a user. The object
is unique per user.
'''
class MessageUser(Base):
    __tablename__ = 'message_user'

    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), primary_key=True)
    nb_unread_messages = d.Column(d.Integer, default=0)
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship(u'User')


t_sf_guard_user_group = d.Table(
    'sf_guard_user_group',
    d.Column('user_id', d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), primary_key=True, nullable=False),
    d.Column('group_id', d.ForeignKey(u'sf_guard_group.id', ondelete=u'CASCADE'), primary_key=True, nullable=False),
)


t_sf_guard_user_permission = d.Table(
    'sf_guard_user_permission',
    d.Column('user_id', d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), primary_key=True, nullable=False),
    d.Column('permission_id', d.ForeignKey(u'sf_guard_permission.id', ondelete=u'CASCADE'), primary_key=True, nullable=False),
)


'''
STATIC: Stores all sports and related Ids
'''
class Sport(Base):
    __tablename__ = 'sport'

    id = d.Column(d.Integer, primary_key=True)
    slug = d.Column(d.String(64))
    name = d.Column(d.String(64))


'''
Deprecated
'''
class UmPhoto(Base):
    __tablename__ = 'um_photo'

    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'))
    body = d.Column(d.Text)

    user = relationship(u'User')


'''
Deprecated
'''
class UmVideo(Base):
    __tablename__ = 'um_video'

    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'))
    url = d.Column(d.String(255))
    title = d.Column(d.String(255))
    youtube_video_id = d.Column(d.String(255))
    vimeo_video_id = d.Column(d.String(255))
    body = d.Column(d.Text)

    user = relationship(u'User')


'''
Represent user follows. This is partially deprecated in favor of
Relate object. But still exist at a lot of places.
'''
class UserConnection(Base):
    __tablename__ = 'user_connection'
    __table_args__ = (
        UniqueConstraint(u'user_id', u'other_user_id', name=u'oneonone'),
        d.Index(u'user_connection_other_user_id_idx', u'other_user_id', unique=False),
        d.Index(u'user_connection_user_id_idx', u'user_id', unique=False),
    )

    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), nullable=False)
    other_user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), nullable=False)
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)

    other_user = relationship(u'User', primaryjoin='UserConnection.other_user_id == User.id', lazy=u'joined')
    user = relationship(u'User', primaryjoin='UserConnection.user_id == User.id', lazy=u'joined')


'''
Also created when the user is created. All email communications to the
user through the system can be configured using these parameters.
'''
class UserEmailPreference(Base):
    __tablename__ = 'user_email_preferences'

    id = d.Column(d.Integer, primary_key=True, nullable=False, unique=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), primary_key=True, nullable=False)
    new_application = d.Column(d.Boolean, default=False)
    new_follower = d.Column(d.Boolean, default=False)
    new_post_like = d.Column(d.Boolean, default=False)
    new_post_message = d.Column(d.Boolean, default=False)
    new_post_share = d.Column(d.Boolean, default=False)
    new_message = d.Column(d.Boolean, default=False)
    recommendations = d.Column(d.Boolean, default=True)
    reminders = d.Column(d.Boolean, default=True)

    user = relationship(u'User')


'''
Updated when a user logs in.  A new entry is created every time.
Although if the user is already logged in, this is not updated
'''
class UserLogin(Base):
    __tablename__ = 'user_login'
    __table_args__ = (
        d.Index(u'user_login_user_id', u'user_id', unique=False),
    )

    id = d.Column(d.Integer, primary_key=True, nullable=False, unique=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), primary_key=True, nullable=False)
    date = d.Column(d.DateTime)

    user = relationship(u'User')


t_user_position = d.Table(
    'user_position',
    d.Column('position_id', d.ForeignKey(u'position.id'), primary_key=True, nullable=False),
    d.Column('user_id', d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), primary_key=True, nullable=False),
)


t_user_sport = d.Table(
    'user_sport',
    d.Column('user_id', d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), primary_key=True, nullable=False),
    d.Column('sport_id', d.ForeignKey(u'sport.id'), primary_key=True, nullable=False),
)


'''
When a user invites someone else via email, an entry is stored here.
'''
class UserInvite(Base):
    __tablename__ = 'user_invite'
    __table_args__ = (
        d.Index(u'user_invite_user_id', u'user_id', unique=False),
    )

    id = d.Column(d.BigInteger, primary_key=True, nullable=False)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), primary_key=True, nullable=False)
    email = d.Column(d.String)
    signed_up = d.Column(d.Boolean, default=False)
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


'''
Started tracking 07/13/2016. Only one last entry is stored per user-visitor combo.
This helps provide better data for users and also avoids spamming on the database.
'''
class UserVisit(Base):
    __tablename__ = 'user_visit'
    __table_args__ = (
        UniqueConstraint(u'user_id', u'visitor_id', name=u'unique_visit'),
    )

    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'))
    visitor_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'))
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship(u'User', primaryjoin='UserVisit.user_id == User.id')
    visitor = relationship(u'User', primaryjoin='UserVisit.visitor_id == User.id')


'''
Used for payment platform. This is used to manage the paid subscriptions of user.
Refer to braintree documentation for plan details. Subscriptions should still work,
although the flow has been hidden.
'''
class UserSubscription(Base):
    __tablename__ = 'user_subscription'

    id = d.Column(d.BigInteger, primary_key=True)
    active = d.Column(d.Boolean, default=True)
    status = d.Column(d.String, default='pending') # Options: pending, active, ended, overdue
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user_id = d.Column(d.ForeignKey(u'sf_guard_user.id', ondelete=u'CASCADE'), nullable=False, index=True)
    plan_type = d.Column(d.String, default='intro')
    plan_length = d.Column(d.String, default='monthly') # Options monthly, annual
    next_payment_due = d.Column(d.Date)
    end_date = d.Column(d.Date) # Only if status = ended
    braintree_customer_id = d.Column(d.String)
    payment_method_token = d.Column(d.String)
    braintree_subscription_id = d.Column(d.String)

    user = relationship(u'User', primaryjoin=u'UserSubscription.user_id == User.id')


'''
Whole platform stats are stored here using a cron everyday.
'''
class DailyStats(Base):
    __tablename__ = 'daily_stats'

    id = d.Column(d.BigInteger, primary_key=True)
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    listings = d.Column(d.Integer, default=0)
    applications = d.Column(d.Integer, default=0)
    users = d.Column(d.Integer, default=0)
    clubs = d.Column(d.Integer, default=0)
    agents = d.Column(d.Integer, default=0)
    athletes = d.Column(d.Integer, default=0)
    unknown_users = d.Column(d.Integer, default=0)
    messages = d.Column(d.Integer, default=0)
    club_messages = d.Column(d.Integer, default=0)
    agent_messages = d.Column(d.Integer, default=0)
    athlete_messages = d.Column(d.Integer, default=0)
    threads = d.Column(d.Integer, default=0)
    club_threads = d.Column(d.Integer, default=0)
    agent_threads = d.Column(d.Integer, default=0)
    athlete_threads = d.Column(d.Integer, default=0)
    connections = d.Column(d.Integer, default=0)
    looking_for = d.Column(d.Integer, default=0)
    posts = d.Column(d.Integer, default=0)

    @property
    def date(self):
        return self.created_at


'''
Similar to DailyStats but this is executed weekly
'''
class WeeklyStats(Base):
    __tablename__ = 'weekly_stats'

    id = d.Column(d.BigInteger, primary_key=True)
    created_at = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    updated_at = d.Column(d.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    start = d.Column(d.DateTime, default=datetime.datetime.utcnow)
    end = d.Column(d.DateTime, default=datetime.datetime.utcnow)

    listings = d.Column(d.Integer, default=0)
    applications = d.Column(d.Integer, default=0)
    users = d.Column(d.Integer, default=0)
    clubs = d.Column(d.Integer, default=0)
    agents = d.Column(d.Integer, default=0)
    athletes = d.Column(d.Integer, default=0)
    unknown_users = d.Column(d.Integer, default=0)
    messages = d.Column(d.Integer, default=0)
    club_messages = d.Column(d.Integer, default=0)
    agent_messages = d.Column(d.Integer, default=0)
    athlete_messages = d.Column(d.Integer, default=0)
    threads = d.Column(d.Integer, default=0)
    club_threads = d.Column(d.Integer, default=0)
    agent_threads = d.Column(d.Integer, default=0)
    athlete_threads = d.Column(d.Integer, default=0)
    connections = d.Column(d.Integer, default=0)
    looking_for = d.Column(d.Integer, default=0)
    posts = d.Column(d.Integer, default=0)

    @property
    def date(self):
        return self.end


'''
Used for unclaimed profiles. Anyone can request a claim for any profile.
We track those using this object. Also, an email is sent for any claim to
mat@ and ankit@
'''
class ClaimProfile(Base):
    __tablename__ = 'claim_profile'

    id = d.Column(d.Integer, primary_key=True)
    user_id = d.Column(d.Integer)
    email = d.Column(d.String)
    name = d.Column(d.String)
    comments = d.Column(d.Text)
    status = d.Column(d.String, default='pending')

