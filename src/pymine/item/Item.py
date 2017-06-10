# coding=utf-8
import json

from pymine.Server import Server
from pymine.block.Block import Block
from pymine.utils.Config import Config
from ..nbt.tag.CompoundTag import *
from ..nbt.NBT import *
from .ItemIds import *


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Item(ItemIds):
    cachedParser = None

    def parseCompoundTag(self, tag: str) -> CompoundTag:
        if (self.cachedParser == None):
            self.cachedParser = NBT(NBT.LITTLE_ENDIAN)

        self.cachedParser.read(tag)
        return self.cachedParser.getData()

    def writeCompoundTag(self, tag: CompoundTag) -> str:
        if (self.cachedParser is None):
            self.cachedParser = NBT(NBT.LITTLE_ENDIAN)

        self.cachedParser.setData(tag)
        return self.cachedParser.write()

    """ @var SplFixedArray """
    list = None
    block = None
    id = None
    meta = None
    tags = ""
    cachedNBT = None

    count = None
    name = None

    @staticmethod
    def canBeActivated():
        return False

    def init(self):
        if self.list is None:
            self.list = [] * 65536
            self.list[self.IRON_SHOVEL] = IronShovel
            self.list[self.IRON_PICKAXE] = IronPickaxe
            self.list[self.IRON_AXE] = IronAxe
            self.list[self.FLINT_STEEL] = FlintSteel
            self.list[self.APPLE] = Apple
            self.list[self.BOW] = Bow
            self.list[self.ARROW] = Arrow
            self.list[self.COAL] = Coal
            self.list[self.DIAMOND] = Diamond
            self.list[self.IRON_INGOT] = IronIngot
            self.list[self.GOLD_INGOT] = GoldIngot
            self.list[self.IRON_SWORD] = IronSword
            self.list[self.WOODEN_SWORD] = WoodenSword
            self.list[self.WOODEN_SHOVEL] = WoodenShovel
            self.list[self.WOODEN_PICKAXE] = WoodenPickaxe
            self.list[self.WOODEN_AXE] = WoodenAxe
            self.list[self.STONE_SWORD] = StoneSword
            self.list[self.STONE_SHOVEL] = StoneShovel
            self.list[self.STONE_PICKAXE] = StonePickaxe
            self.list[self.STONE_AXE] = StoneAxe
            self.list[self.DIAMOND_SWORD] = DiamondSword
            self.list[self.DIAMOND_SHOVEL] = DiamondShovel
            self.list[self.DIAMOND_PICKAXE] = DiamondPickaxe
            self.list[self.DIAMOND_AXE] = DiamondAxe
            self.list[self.STICK] = Stick
            self.list[self.BOWL] = Bowl
            self.list[self.MUSHROOM_STEW] = MushroomStew
            self.list[self.GOLD_SWORD] = GoldSword
            self.list[self.GOLD_SHOVEL] = GoldShovel
            self.list[self.GOLD_PICKAXE] = GoldPickaxe
            self.list[self.GOLD_AXE] = GoldAxe
            self.list[self.STRING] = StringItem
            self.list[self.FEATHER] = Feather
            self.list[self.GUNPOWDER] = Gunpowder
            self.list[self.WOODEN_HOE] = WoodenHoe
            self.list[self.STONE_HOE] = StoneHoe
            self.list[self.IRON_HOE] = IronHoe
            self.list[self.DIAMOND_HOE] = DiamondHoe
            self.list[self.GOLD_HOE] = GoldHoe
            self.list[self.WHEAT_SEEDS] = WheatSeeds
            self.list[self.WHEAT] = Wheat
            self.list[self.BREAD] = Bread
            self.list[self.LEATHER_CAP] = LeatherCap
            self.list[self.LEATHER_TUNIC] = LeatherTunic
            self.list[self.LEATHER_PANTS] = LeatherPants
            self.list[self.LEATHER_BOOTS] = LeatherBoots
            self.list[self.CHAIN_HELMET] = ChainHelmet
            self.list[self.CHAIN_CHESTPLATE] = ChainChestplate
            self.list[self.CHAIN_LEGGINGS] = ChainLeggings
            self.list[self.CHAIN_BOOTS] = ChainBoots
            self.list[self.IRON_HELMET] = IronHelmet
            self.list[self.IRON_CHESTPLATE] = IronChestplate
            self.list[self.IRON_LEGGINGS] = IronLeggings
            self.list[self.IRON_BOOTS] = IronBoots
            self.list[self.DIAMOND_HELMET] = DiamondHelmet
            self.list[self.DIAMOND_CHESTPLATE] = DiamondChestplate
            self.list[self.DIAMOND_LEGGINGS] = DiamondLeggings
            self.list[self.DIAMOND_BOOTS] = DiamondBoots
            self.list[self.GOLD_HELMET] = GoldHelmet
            self.list[self.GOLD_CHESTPLATE] = GoldChestplate
            self.list[self.GOLD_LEGGINGS] = GoldLeggings
            self.list[self.GOLD_BOOTS] = GoldBoots
            self.list[self.FLINT] = Flint
            self.list[self.RAW_PORKCHOP] = RawPorkchop
            self.list[self.COOKED_PORKCHOP] = CookedPorkchop
            self.list[self.PAINTING] = Painting
            self.list[self.GOLDEN_APPLE] = GoldenApple
            self.list[self.SIGN] = Sign
            self.list[self.WOODEN_DOOR] = WoodenDoor
            self.list[self.SPRUCE_DOOR] = SpruceDoor
            self.list[self.BIRCH_DOOR] = BirchDoor
            self.list[self.JUNGLE_DOOR] = JungleDoor
            self.list[self.ACACIA_DOOR] = AcaciaDoor
            self.list[self.DARK_OAK_DOOR] = DarkOakDoor
            self.list[self.BUCKET] = Bucket
            self.list[self.MINECART] = Minecart
            self.list[self.IRON_DOOR] = IronDoor
            self.list[self.REDSTONE] = Redstone
            self.list[self.SNOWBALL] = Snowball
            self.list[self.BOAT] = Boat
            self.list[self.LEATHER] = Leather
            self.list[self.BRICK] = Brick
            self.list[self.CLAY] = Clay
            self.list[self.SUGARCANE] = Sugarcane
            self.list[self.PAPER] = Paper
            self.list[self.BOOK] = Book
            self.list[self.SLIMEBALL] = Slimeball
            self.list[self.EGG] = Egg
            self.list[self.COMPASS] = Compass
            self.list[self.FISHING_ROD] = FishingRod
            self.list[self.CLOCK] = Clock
            self.list[self.GLOWSTONE_DUST] = GlowstoneDust
            self.list[self.RAW_FISH] = Fish
            self.list[self.COOKED_FISH] = CookedFish
            self.list[self.DYE] = Dye
            self.list[self.BONE] = Bone
            self.list[self.SUGAR] = Sugar
            self.list[self.CAKE] = Cake
            self.list[self.BED] = Bed
            self.list[self.COOKIE] = Cookie
            self.list[self.FILLED_MAP] = FilledMap
            self.list[self.EMPTY_MAP] = EmptyMap
            self.list[self.SHEARS] = Shears
            self.list[self.MELON] = Melon
            self.list[self.PUMPKIN_SEEDS] = PumpkinSeeds
            self.list[self.MELON_SEEDS] = MelonSeeds
            self.list[self.RAW_BEEF] = RawBeef
            self.list[self.STEAK] = Steak
            self.list[self.RAW_CHICKEN] = RawChicken
            self.list[self.COOKED_CHICKEN] = CookedChicken
            self.list[self.GOLD_NUGGET] = GoldNugget
            self.list[self.NETHER_WART] = NetherWart
            self.list[self.POTION] = Potion
            self.list[self.GLASS_BOTTLE] = GlassBottle
            self.list[self.SPIDER_EYE] = SpiderEye
            self.list[self.FERMENTED_SPIDER_EYE] = FermentedSpiderEye
            self.list[self.BLAZE_POWDER] = BlazePowder
            self.list[self.MAGMA_CREAM] = MagmaCream
            self.list[self.BREWING_STAND] = BrewingStand
            self.list[self.GLISTERING_MELON] = GlisteringMelon
            self.list[self.SPAWN_EGG] = SpawnEgg
            self.list[self.EMERALD] = Emerald
            self.list[self.ITEM_FRAME] = ItemFrame
            self.list[self.FLOWER_POT] = FlowerPot
            self.list[self.CARROT] = Carrot
            self.list[self.POTATO] = Potato
            self.list[self.BAKED_POTATO] = BakedPotato
            self.list[self.GOLDEN_CARROT] = GoldenCarrot
            self.list[self.MOB_HEAD] = MobHead
            self.list[self.PUMPKIN_PIE] = PumpkinPie
            self.list[self.NETHER_BRICK] = NetherBrick
            self.list[self.QUARTZ] = Quartz
            self.list[self.QUARTZ] = NetherQuartz
            self.list[self.COOKED_RABBIT] = CookedRabbit
            self.list[self.CAMERA] = Camera
            self.list[self.BEETROOT] = Beetroot
            self.list[self.BEETROOT_SEEDS] = BeetrootSeeds
            self.list[self.BEETROOT_SOUP] = BeetrootSoup
            self.list[self.PRISMARINE_SHARD] = PrismarineShard
            self.list[self.PRISMARINE_CRYSTALS] = PrismarineCrystals
            self.list[self.NETHER_STAR] = NetherStar
            self.list[self.ENCHANTED_GOLDEN_APPLE] = GoldenAppleEnchanted
            self.list[self.ENDER_PEARL] = EnderPearl
            self.list[self.EYE_OF_ENDER] = EyeOfEnder
            self.list[self.DRAGON_BREATH] = DragonBreath
            self.list[self.POPPED_CHORUS_FRUIT] = PoppedChorusFruit
            self.list[self.CHORUS_FRUIT] = ChorusFruit
            self.list[self.ELYTRA] = Elytra
            self.list[self.SHULKER_SHELL] = ShulkerShell
            self.list[self.ENCHANTING_BOTTLE] = EnchantingBottle
            self.list[self.HOPPER] = Hopper

            for i in range(256):
                if Block.list[i] is not None:
                    self.list[i] = Block.list[i]

        self.initCreativeItems()

    creative = []

    def initCreativeItems(self):
        self.clearCreativeItems()

        creativeItems = Config(Server.getInstance().getFilePath() + "src/pocketmine/resources/creativeitems.json", Config.JSON, [])

        for data in creativeItems.getAll():
            item = Item.get(data["id"], data["damage"], data["count"], data["nbt"])
            if (item.getName() == "Unknown"):
                continue

            self.addCreativeItem(item)


def clearCreativeItems()

    {
        Item.creative = []

    def getCreativeItems() -> array

    {

    return Item.creative

}

def addCreativeItem(Item item

){
    Item.creative[] = clone
item
}

def removeCreativeItem(Item item

){
    index = self.getCreativeItemIndex(item)
if (index != -1)
{
    unset(Item.creative[index])
}
}

def isCreativeItem(Item item

) -> bool
{
    foreach(Item.creative as i = > d){
if (item.equals(d, !item.isTool())){
return True
}
}

return False
}

"""
# param index
           *
           #
return Item
"""


def getCreativeItem(int index

){
return Item.creative[index] ?? None
}

def getCreativeItemIndex(Item item

) -> int
{
    foreach(Item.creative as i = > d){
if (item.equals(d, !item.isTool())){
return i
}
}

return -1
}

"""
*Returns
an
instance
of
the
Item
with the specified id, meta, count and NBT.
*
# param int                id
# param int                meta
# param int                count
# param CompoundTag | string tags
*
#
return Item
"""


def get(int id, int


meta = 0, int
count = 1, tags = "") -> Item
{
try{


class = self.


list[id]
if (


class == None){


return (
    Item(id, meta, count)).setCompoundTag(tags)
} elif (id < 256)
{
return (
    ItemBlock(


class(meta), meta, count)).setCompoundTag(tags)
}else{


return (


class(meta, count)).setCompoundTag(tags)
}
}catch(\RuntimeException e){


return (
    Item(id, meta, count)).setCompoundTag(tags)
}
}

"""
# param
string str
        # param
bool   multiple
        *
        #
return Item[] | Item
"""


def fromString(string str, bool


multiple = False){
if (multiple == True)
{
    blocks = []
foreach(explode(",", str) as b){
    blocks[] = self.fromString(b, False)
}

return blocks
}else{
b = explode(":", str_replace([" ", "minecraft:"], ["_", ""], trim(str)))
if (!isset(b[1])){
meta = 0
}else{
meta = b[1] & 0xFFFF
}

if (defined(Item + ".".strtoupper(b[0]))){
item = self.

get(constant(Item + ".".strtoupper(b[0])), meta)
if (item.getId() == self.

AIR and strtoupper(b[0]) != "AIR"){
item = self.get(b[0] & 0xFFFF, meta)
}
}else{
item = self.get(b[0] & 0xFFFF, meta)
}

return item
}
}

"""
# param
int id
     # param
int meta
     # param
int count
     # param
string name
        """


def __construct(int id, int


meta = 0, int
count = 1, string
name = "Unknown"){
    this.id = id & 0xffff
this.meta = meta != -1 ? meta & 0xffff: -1
this.count = count
this.name = name
if (!isset(this.block) and this.id <= 0xff and isset(Block.list[this.id])){
    this.block = Block.get(this.id, this.meta)
this.name = this.block.getName()
}
}

"""
*Sets
the
Item
's NBT
*
# param
CompoundTag | string tags
                      *
                      #
return this
"""


def setCompoundTag(tags){
if (tags


instanceof
CompoundTag){
    this.setNamedTag(tags)
}else{
    this.tags = (string)
tags
this.cachedNBT = None
}

return this
}

"""
*Returns
the
serialized
NBT
of
the
Item
#
return string
"""


def getCompoundTag() -> string

:


return this.tags
}

"""
*Returns
whether
this
Item
has
a
non - empty
NBT.
#
return bool
"""


def hasCompoundTag() -> bool


{
return this.tags != ""
}

"""
# return bool
"""


def hasCustomBlockData() -> bool


{
if (!this.hasCompoundTag()){
return False
}

tag = this.getNamedTag()
if (isset(tag.BlockEntityTag) and tag.BlockEntityTag
instanceof
CompoundTag){
return True
}

return False
}

def clearCustomBlockData()

:
if (!this.hasCompoundTag()){

return this
}
tag = this.getNamedTag()

if (isset(tag.BlockEntityTag) and tag.BlockEntityTag
instanceof
CompoundTag){
unset(tag.display.BlockEntityTag)
this.setNamedTag(tag)
}

return this
}

"""
# param
CompoundTag compound
             *
             #
return this
"""


def setCustomBlockData(CompoundTag compound

){
    tags = clone
compound
tags.setName("BlockEntityTag")

if (!this.hasCompoundTag()){
    tag =
CompoundTag("", [])
}else{
    tag = this.getNamedTag()
}

tag.BlockEntityTag = tags
this.setNamedTag(tag)

return this
}

"""
# return CompoundTag | None
"""


def getCustomBlockData()

:
if (!this.hasCompoundTag()){

return None
}

tag = this.getNamedTag()
if (isset(tag.BlockEntityTag) and tag.BlockEntityTag
instanceof
CompoundTag){
return tag.BlockEntityTag
}

return None
}

"""
# return bool
"""


def hasEnchantments() -> bool


{
if (!this.hasCompoundTag()){
return False
}

tag = this.getNamedTag()
if (isset(tag.ench))
{
tag = tag.ench
if (tag instanceof ListTag){
return True
}
}

return False
}

"""
# param
int id
     *
     #
return Enchantment | None
"""


def getEnchantment(int id

){
if (!this.hasEnchantments()){
return None
}

foreach(this.getNamedTag().ench as entry){
if (entry["id"] == id){
e = Enchantment.
getEnchantment(entry["id"])
e.setLevel(entry["lvl"])
return e
}
}

return None
}

def getEnchantmentLevel(int id

){
if (!this.hasEnchantments()){
return None
}

foreach(this.getNamedTag().ench as entry){
if (entry["id"] == id){
return entry["lvl"]
}
}

return 0
}

"""
# param
Enchantment ench
             """


def addEnchantment(Enchantment ench

){
if (!this.hasCompoundTag()){
    tag =
CompoundTag("", [])
}else{
    tag = this.getNamedTag()
}

if (!isset(tag.ench)){
tag.ench =  ListTag("ench", [])
tag.ench.setTagType(NBT.
TAG_Compound)
}

found = False

foreach(tag.ench as k = > entry){
if (entry["id"] == ench.getId()){
tag.ench.{k} =
CompoundTag("", [
"id" = >
ShortTag("id", ench.getId()),
"lvl" = >
ShortTag("lvl", ench.getLevel())
])
found = True
break
}
}

if (!found){
tag.ench.{count(tag.ench) + 1} =  CompoundTag("", [
"id" = > ShortTag("id", ench.getId()),
"lvl" = > ShortTag("lvl", ench.getLevel())
])
}

this.setNamedTag(tag)
}

"""
#
return Enchantment[]
"""


def getEnchantments() -> array


{
if (!this.hasEnchantments()){
return []
}

enchantments = []

foreach(this.getNamedTag().ench as entry){
e = Enchantment.getEnchantment(entry["id"])
e.setLevel(entry["lvl"])
enchantments[] = e
}

return enchantments
}

"""
# return bool
"""


def hasCustomName() -> bool


{
if (!this.hasCompoundTag()){
return False
}

tag = this.getNamedTag()
if (isset(tag.display))
{
tag = tag.display
if (tag instanceof CompoundTag and isset(tag.Name) and tag.Name instanceof StringTag){
return True
}
}

return False
}

"""
# return string
"""


def getCustomName() -> string

:
if (!this.hasCompoundTag()){

return ""
}

tag = this.getNamedTag()
if (isset(tag.display))
{
tag = tag.display
if (tag instanceof CompoundTag and isset(tag.Name) and tag.Name instanceof StringTag){
return tag.Name.getValue()
}
}

return ""
}

"""
# param
string name
        *
        #
return this
"""


def setCustomName(string name

){
if (name == "")
{
    this.clearCustomName()
}

if (!this.hasCompoundTag()){
    tag =
CompoundTag("", [])
}else{
    tag = this.getNamedTag()
}

if (isset(tag.display) and tag.display instanceof CompoundTag){
tag.display.Name =  StringTag("Name", name)
}else{
tag.display =  CompoundTag("display", [
"Name" = > StringTag("Name", name)
])
}

this.setCompoundTag(tag)

return this
}

"""
# return this
"""


def clearCustomName()

:
if (!this.hasCompoundTag()){

return this
}
tag = this.getNamedTag()

if (isset(tag.display) and tag.display
instanceof
CompoundTag){
unset(tag.display.Name)
if (tag.display.getCount() == 0){
unset(tag.display)
}

this.setNamedTag(tag)
}

return this
}

"""
# param name
           #
return Tag | None
"""


def getNamedTagEntry(name){
    tag = this.getNamedTag()
if (tag != None)


{
return tag.
{name} ?? None
}

return None
}

"""
*Returns
a
tree
of
Tag
objects
representing
the
Item
's NBT
#
return None | CompoundTag
"""


def getNamedTag()

:
if (!this.hasCompoundTag()){

return None
} elif (this.cachedNBT != None)
{
return this.cachedNBT
}
return this.cachedNBT = self.parseCompoundTag(this.tags)
}

"""
*Sets
the
Item
's NBT from the supplied CompoundTag object.
# param
CompoundTag tag
             *
             #
return this
"""


def setNamedTag(CompoundTag tag

){
if (tag.getCount() == 0)
{
return this.clearNamedTag()
}

this.cachedNBT = tag
this.tags = self.writeCompoundTag(tag)

return this
}

"""
*Removes
the
Item
's NBT.
#
return Item
"""


def clearNamedTag()

:


return this.setCompoundTag("")
}

"""
# return int
"""


def getCount() -> int


{
return this.count
}

"""
# param
int count
     """


def setCount(int count

){
    this.count = count
}

"""
*Returns
the
name
of
the
item, or the
custom
name if it is set.
              #
return string
"""
final


def getName() -> string

:


return this.hasCustomName() ? this.getCustomName() -> this.name
}

"""
# return bool
"""
final


def canBePlaced() -> bool


{
return this.block != None and this.block.canBePlaced()
}

"""
*Returns
whether
an
entity
can
eat or drink
this
item.
#
return bool
"""


def canBeConsumed() -> bool


{
return False
}

"""
*Returns
whether
this
item
can
be
consumed
by
the
supplied
Entity.
# param
Entity entity
        *
        #
return bool
"""


def canBeConsumedBy(Entity entity

) -> bool
{
return this.canBeConsumed()
}

"""
*Called
when
the
item is consumed
by
an
Entity.
# param
Entity entity
        """


def onConsume(Entity entity

){

}

"""
*Returns
the
block
corresponding
to
this
Item.
#
return Block
"""


def getBlock() -> Block


{
if (this.block
instanceof
Block){
return clone
this.block
}else{
return Block.get(self.AIR)
}
}

"""
# return int
"""
final


def getId() -> int


{
return this.id
}

"""
# return int
"""
final


def getDamage() -> int


{
return this.meta
}

"""
# param
int meta
     """


def setDamage(int meta

){
    this.meta = meta != -1 ? meta & 0xFFFF: -1
}

"""
*Returns
whether
this
item
can
match
any
item
with an equivalent ID with any meta value.
* Used in crafting recipes which accept multiple variants of the same item, for example crafting tables recipes.
*
#
return bool
"""


def hasAnyDamageValue() -> bool


{
return this.meta == -1
}

"""
*Returns
the
highest
amount
of
this
item
which
will
fit
into
one
inventory
slot.
#
return int
"""


def getMaxStackSize()

:


return 64
}

final


def getFuelTime()

:
if (!isset(Fuel.duration[this.id])){

return None
}
if (this.id != self.
    BUCKET or this.meta == 10){
return Fuel.duration[this.id]
}

return None
}

"""
# param
Entity | Block object
                *
                #
return bool
"""


def useOn(object){


return False
}

"""
# return bool
"""


def isTool()

:


return False
}

"""
# return int | bool
"""


def getMaxDurability()

:


return False
}

def isPickaxe()

:


return False
}

def isAxe()

:


return False
}

def isSword()

:


return False
}

def isShovel()

:


return False
}

def isHoe()

:


return False
}

def isShears()

:


return False
}

def getDestroySpeed(Block block, Player


player){
return 1
}

"""
*Called
when
a
player
uses
this
item
on
a
block.
*
# param
Level level
       # param
Player player
        # param
Block block
       # param
Block target
       # param
int face
     # param
float fx
       # param
float fy
       # param
float fz
       *
       #
return bool
"""


def onActivate(Level level, Player


player, Block
block, Block
target, face, fx, fy, fz){
return False
}

"""
*Compares
an
Item
to
this
Item and check if they
match.
*
# param
Item item
      # param
bool checkDamage
Whether
to
verify
that
the
damage
values
match.
# param
bool checkCompound
Whether
to
verify
that
the
items
' NBT match.
*
#
return bool
"""


def equals(Item
    item, bool


checkDamage = True, bool
checkCompound = True) -> bool
{
if (this.id == item.getId() and (checkDamage == False or this.getDamage() == item.getDamage()))
{
if (checkCompound)
{
if (item.getCompoundTag() == this.getCompoundTag())
{
return True
} elif (this.hasCompoundTag() and item.hasCompoundTag())
{
# Serialized NBT didn 't match, check the cached object tree.
return NBT.matchTree(this.getNamedTag(), item.getNamedTag())
}
}else{
return True
}
}

return False
}

"""
# deprecated
Use
{ @ link
Item  # equals} instead, this method will be removed in the future.
*
# param
Item item
# param
bool checkDamage
# param
bool checkCompound
*
# return bool
"""


def deepEquals(Item
    item, bool


checkDamage = True, bool
checkCompound = True) -> bool
{
return this.equals(item, checkDamage, checkCompound)
}

"""
# return string
"""
final


def __toString() -> string

:


return "Item ".this.name.
" (".this.id.
":".(this.hasAnyDamageValue() ? "?": this.meta).")x".this.count.(this.hasCompoundTag() ? " tags:0x".bin2hex(
    this.getCompoundTag()) -> "")
}

"""
*Returns
an
array
of
item
stack
properties
that
can
be
serialized
to
json.
*
#
return array
"""
final


def jsonSerialize()

:


return [
    "id" = > this.id,
             "damage" = > this.meta,
                          "count" = > this.count,  # TODO: separate
                                      items and stacks
"nbt" = > this.tags
]
}

"""
*Serializes
the
item
to
an
NBT
CompoundTag
*
# param
int    slot
optional, the
inventory
slot
of
the
item
# param
string tagName
the
name
to
assign
to
the
CompoundTag
object
*
#
return CompoundTag
"""


def nbtSerialize(int slot = -1, string


tagName = "") -> CompoundTag
{
    tag =
CompoundTag(tagName, [
    "id" = >
ShortTag("id", this.id),
"Count" = >
ByteTag("Count", this.count ?? -1),
"Damage" = >
ShortTag("Damage", this.meta),
])

if (this.hasCompoundTag()){
tag.tag = clone this.getNamedTag()
tag.tag.setName("tag")
}

if (slot != -1){
tag.Slot =  ByteTag("Slot", slot)
}

return tag
}

"""
*Deserializes
an
Item
from an NBT

CompoundTag
*
# param
CompoundTag tag
             *
             #
return Item
"""


def nbtDeserialize(CompoundTag tag

) -> Item
{
if (!isset(tag.id) or !isset(tag.Count)){
return Item.get(0)
}

if (tag.id instanceof ShortTag){
item = Item.get(tag.id.getValue(), !isset(tag.Damage) ? 0: tag.Damage.getValue(), tag.Count.getValue())
} elif (tag.id
instanceof
StringTag){  # PC
item
save
format
item = Item.fromString(tag.id.getValue())
item.setDamage(!isset(tag.Damage) ? 0: tag.Damage.getValue())
item.setCount(tag.Count.getValue())
}else{
throw
\InvalidArgumentException(
    "Item CompoundTag ID must be an instance of StringTag or ShortTag, ".get_class(tag.id).
" given")
}

if (isset(tag.tag) and tag.tag instanceof CompoundTag){
item.setNamedTag(tag.tag)
}

return item
}

def __clone()

:
if (this.block != None):
    this.block = clone
this.block

this.cachedNBT = None
