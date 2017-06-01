from ..entity.Entity import *
from .Air import *
from ..Player import *
from ..item.Item import *
from ..block import *
from ..metadata.Metadatable import *
from ..level.Position import *
from ..math.Vector3 import *
from ...spl.stubs.Core import *


class Block(BlockIds, Metadatable, Position):
    list = None
    fullList = None
    light = None
    ligthFilter = None
    solid = None
    hardness = None
    transparent = None

    id = None
    meta = 0

    boundingBox = None

    def init(self):
        if self.list is None:
            self.list = []
            self.fullList = []
            self.light = []
            self.ligthFilter = []
            self.solid = []
            self.hardness = []
            self.transparent = []

            self.list[BlockIds.ACACIA_DOOR_BLOCK] = AcaciaDoor
            #             self.list[BlockIds.AIR] = Air
            #             self.list[BlockIds.STONE] = Stone
            #             self.list[BlockIds.GRASS] = Grass
            #             self.list[BlockIds.DIRT] = Dirt
            #             self.list[BlockIds.COBBLESTONE] = Cobblestone
            #             self.list[BlockIds.PLANKS] = Planks
            #             self.list[BlockIds.SAPLING] = Sapling
            #             self.list[BlockIds.BEDROCK] = Bedrock
            #             self.list[BlockIds.WATER] = Water
            #             self.list[BlockIds.STILL_WATER] = StillWater
            #             self.list[BlockIds.LAVA] = Lava
            #             self.list[BlockIds.STILL_LAVA] = StillLava
            #             self.list[BlockIds.SAND] = Sand
            #             self.list[BlockIds.GRAVEL] = Gravel
            #             self.list[BlockIds.GOLD_ORE] = GoldOre
            #             self.list[BlockIds.IRON_ORE] = IronOre
            #             self.list[BlockIds.COAL_ORE] = CoalOre
            #             self.list[BlockIds.WOOD] = Wood
            #             self.list[BlockIds.LEAVES] = Leaves
            #             self.list[BlockIds.SPONGE] = Sponge
            #             self.list[BlockIds.GLASS] = Glass
            #             self.list[BlockIds.LAPIS_ORE] = LapisOre
            #             self.list[BlockIds.LAPIS_BLOCK] = Lapis
            self.list[BlockIds.ACTIVATOR_RAIL] = ActivatorRail
            #             self.list[BlockIds.COCOA_BLOCK] = CocoaBlock
            #             self.list[BlockIds.SANDSTONE] = Sandstone
            #             self.list[BlockIds.NOTE_BLOCK] = NoteBlock
            #             self.list[BlockIds.BED_BLOCK] = Bed
            #             self.list[BlockIds.POWERED_RAIL] = PoweredRail
            #             self.list[BlockIds.DETECTOR_RAIL] = DetectorRail
            #             self.list[BlockIds.COBWEB] = Cobweb
            #             self.list[BlockIds.TALL_GRASS] = TallGrass
            #             self.list[BlockIds.DEAD_BUSH] = DeadBush
            #             self.list[BlockIds.WOOL] = Wool
            #             self.list[BlockIds.DANDELION] = Dandelion
            #             self.list[BlockIds.RED_FLOWER] = Flower
            #             self.list[BlockIds.BROWN_MUSHROOM] = BrownMushroom
            #             self.list[BlockIds.RED_MUSHROOM] = RedMushroom
            #             self.list[BlockIds.GOLD_BLOCK] = Gold
            #             self.list[BlockIds.IRON_BLOCK] = Iron
            #             self.list[BlockIds.DOUBLE_SLAB] = DoubleSlab
            #             self.list[BlockIds.SLAB] = Slab
            #             self.list[BlockIds.BRICKS_BLOCK] = Bricks
            #             self.list[BlockIds.TNT] = TNT
            #             self.list[BlockIds.BOOKSHELF] = Bookshelf
            #             self.list[BlockIds.MOSS_STONE] = MossStone
            #             self.list[BlockIds.OBSIDIAN] = Obsidian
            #             self.list[BlockIds.TORCH] = Torch
            #             self.list[BlockIds.FIRE] = Fire
            #             self.list[BlockIds.MONSTER_SPAWNER] = MonsterSpawner
            #             self.list[BlockIds.WOOD_STAIRS] = WoodStairs
            #             self.list[BlockIds.CHEST] = Chest
            #
            #             self.list[BlockIds.DIAMOND_ORE] = DiamondOre
            #             self.list[BlockIds.DIAMOND_BLOCK] = Diamond
            #             self.list[BlockIds.WORKBENCH] = Workbench
            #             self.list[BlockIds.WHEAT_BLOCK] = Wheat
            #             self.list[BlockIds.FARMLAND] = Farmland
            #             self.list[BlockIds.FURNACE] = Furnace
            #             self.list[BlockIds.BURNING_FURNACE] = BurningFurnace
            #             self.list[BlockIds.SIGN_POST] = SignPost
            #             self.list[BlockIds.WOOD_DOOR_BLOCK] = WoodDoor
            #             self.list[BlockIds.SPRUCE_DOOR_BLOCK] = SpruceDoor
            #             self.list[BlockIds.BIRCH_DOOR_BLOCK] = BirchDoor
            #             self.list[BlockIds.JUNGLE_DOOR_BLOCK] = JungleDoor
            #             self.list[BlockIds.DARK_OAK_DOOR_BLOCK] = DarkOakDoor
            #             self.list[BlockIds.LADDER] = Ladder
            #             self.list[BlockIds.RAIL] = Rail
            #
            #             self.list[BlockIds.COBBLESTONE_STAIRS] = CobblestoneStairs
            #             self.list[BlockIds.WALL_SIGN] = WallSign
            #             self.list[BlockIds.LEVER] = Lever
            #             self.list[BlockIds.STONE_PRESSURE_PLATE] = StonePressurePlate
            #             self.list[BlockIds.IRON_DOOR_BLOCK] = IronDoor
            #             self.list[BlockIds.WOODEN_PRESSURE_PLATE] = WoodenPressurePlate
            #             self.list[BlockIds.REDSTONE_ORE] = RedstoneOre
            #             self.list[BlockIds.GLOWING_REDSTONE_ORE] = GlowingRedstoneOre
            #
            #             self.list[BlockIds.REDSTONE_TORCH] = RedstoneTorch
            #             self.list[BlockIds.LIT_REDSTONE_TORCH] = LitRedstoneTorch
            #             self.list[BlockIds.STONE_BUTTON] = StoneButton
            #             self.list[BlockIds.SNOW_LAYER] = SnowLayer
            #             self.list[BlockIds.ICE] = Ice
            #             self.list[BlockIds.SNOW_BLOCK] = Snow
            #             self.list[BlockIds.CACTUS] = Cactus
            #             self.list[BlockIds.CLAY_BLOCK] = Clay
            #             self.list[BlockIds.SUGARCANE_BLOCK] = Sugarcane
            #
            #             self.list[BlockIds.FENCE] = Fence
            #             self.list[BlockIds.PUMPKIN] = Pumpkin
            #             self.list[BlockIds.NETHERRACK] = Netherrack
            #             self.list[BlockIds.SOUL_SAND] = SoulSand
            #             self.list[BlockIds.GLOWSTONE_BLOCK] = Glowstone
            #
            #             self.list[BlockIds.LIT_PUMPKIN] = LitPumpkin
            #             self.list[BlockIds.CAKE_BLOCK] = Cake
            #
            #             self.list[BlockIds.TRAPDOOR] = Trapdoor
            #
            #             self.list[BlockIds.STONE_BRICKS] = StoneBricks
            #
            #             self.list[BlockIds.IRON_BARS] = IronBars
            #             self.list[BlockIds.GLASS_PANE] = GlassPane
            #             self.list[BlockIds.MELON_BLOCK] = Melon
            #             self.list[BlockIds.PUMPKIN_STEM] = PumpkinStem
            #             self.list[BlockIds.MELON_STEM] = MelonStem
            #             self.list[BlockIds.VINE] = Vine
            #             self.list[BlockIds.FENCE_GATE] = FenceGate
            #             self.list[BlockIds.BRICK_STAIRS] = BrickStairs
            #             self.list[BlockIds.STONE_BRICK_STAIRS] = StoneBrickStairs
            #
            #             self.list[BlockIds.MYCELIUM] = Mycelium
            #             self.list[BlockIds.WATER_LILY] = WaterLily
            #             self.list[BlockIds.NETHER_BRICKS] = NetherBrick
            #             self.list[BlockIds.NETHER_BRICK_FENCE] = NetherBrickFence
            #             self.list[BlockIds.NETHER_BRICKS_STAIRS] = NetherBrickStairs
            #
            #             self.list[BlockIds.ENCHANTING_TABLE] = EnchantingTable
            #             self.list[BlockIds.BREWING_STAND_BLOCK] = BrewingStand
            #             self.list[BlockIds.END_PORTAL] = EndPortal
            #             self.list[BlockIds.END_PORTAL_FRAME] = EndPortalFrame
            #             self.list[BlockIds.END_STONE] = EndStone
            #             self.list[BlockIds.END_STONE_BRICKS] = EndStoneBricks
            #             self.list[BlockIds.REDSTONE_LAMP] = RedstoneLamp
            #             self.list[BlockIds.LIT_REDSTONE_LAMP] = LitRedstoneLamp
            #             self.list[BlockIds.SANDSTONE_STAIRS] = SandstoneStairs
            #             self.list[BlockIds.EMERALD_ORE] = EmeraldOre
            #             self.list[BlockIds.ENDER_CHEST] = EnderChest
            #             self.list[BlockIds.TRIPWIRE_HOOK] = TripwireHook
            #             self.list[BlockIds.TRIPWIRE] = Tripwire
            #             self.list[BlockIds.EMERALD_BLOCK] = Emerald
            #             self.list[BlockIds.SPRUCE_WOOD_STAIRS] = SpruceWoodStairs
            #             self.list[BlockIds.BIRCH_WOOD_STAIRS] = BirchWoodStairs
            #             self.list[BlockIds.JUNGLE_WOOD_STAIRS] = JungleWoodStairs
            #             self.list[BlockIds.BEACON] = Beacon
            #             self.list[BlockIds.STONE_WALL] = StoneWall
            #             self.list[BlockIds.FLOWER_POT_BLOCK] = FlowerPot
            #             self.list[BlockIds.CARROT_BLOCK] = Carrot
            #             self.list[BlockIds.POTATO_BLOCK] = Potato
            #             self.list[BlockIds.WOODEN_BUTTON] = WoodenButton
            #             self.list[BlockIds.MOB_HEAD_BLOCK] = MobHead
            #             self.list[BlockIds.ANVIL] = Anvil
            #             self.list[BlockIds.TRAPPED_CHEST] = TrappedChest
            #             self.list[BlockIds.WEIGHTED_PRESSURE_PLATE_LIGHT] = WeightedPressurePlateLight
            #             self.list[BlockIds.WEIGHTED_PRESSURE_PLATE_HEAVY] = WeightedPressurePlateHeavy
            #
            #             self.list[BlockIds.DAYLIGHT_SENSOR] = DaylightSensor
            #             self.list[BlockIds.REDSTONE_BLOCK] = Redstone
            #
            #             self.list[BlockIds.COMMAND_BLOCK] = CommandBlock
            #             self.list[BlockIds.QUARTZ_BLOCK] = Quartz
            #             self.list[BlockIds.QUARTZ_STAIRS] = QuartzStairs
            #             self.list[BlockIds.DOUBLE_WOOD_SLAB] = DoubleWoodSlab
            #             self.list[BlockIds.WOOD_SLAB] = WoodSlab
            #             self.list[BlockIds.STAINED_CLAY] = StainedClay
            #
            #             self.list[BlockIds.LEAVES2] = Leaves2
            #             self.list[BlockIds.WOOD2] = Wood2
            #             self.list[BlockIds.ACACIA_WOOD_STAIRS] = AcaciaWoodStairs
            #             self.list[BlockIds.DARK_OAK_WOOD_STAIRS] = DarkOakWoodStairs
            #             self.list[BlockIds.PRISMARINE] = Prismarine
            #             self.list[BlockIds.SEA_LANTERN] = SeaLantern
            #             self.list[BlockIds.IRON_TRAPDOOR] = IronTrapdoor
            #             self.list[BlockIds.HAY_BALE] = HayBale
            #             self.list[BlockIds.CARPET] = Carpet
            #             self.list[BlockIds.HARDENED_CLAY] = HardenedClay
            #             self.list[BlockIds.COAL_BLOCK] = Coal
            #             self.list[BlockIds.PACKED_ICE] = PackedIce
            #             self.list[BlockIds.DOUBLE_PLANT] = DoublePlant
            #
            #             self.list[BlockIds.FENCE_GATE_SPRUCE] = FenceGateSpruce
            #             self.list[BlockIds.FENCE_GATE_BIRCH] = FenceGateBirch
            #             self.list[BlockIds.FENCE_GATE_JUNGLE] = FenceGateJungle
            #             self.list[BlockIds.FENCE_GATE_DARK_OAK] = FenceGateDarkOak
            #             self.list[BlockIds.FENCE_GATE_ACACIA] = FenceGateAcacia
            #
            #             self.list[BlockIds.ITEM_FRAME_BLOCK] = ItemFrame
            #
            #             self.list[BlockIds.GRASS_PATH] = GrassPath
            #
            #             self.list[BlockIds.PODZOL] = Podzol
            #             self.list[BlockIds.BEETROOT_BLOCK] = Beetroot
            #             self.list[BlockIds.STONECUTTER] = Stonecutter
            #             self.list[BlockIds.GLOWING_OBSIDIAN] = GlowingObsidian
            #
            #             self.list[BlockIds.HOPPER_BLOCK] = Hopper
            #                 self.list[BlockIds.DRAGON_EGG] = DragonEgg
            #             self.list[BlockIds.CHORUS_FLOWER] = ChorusFlower
            #              self.list[BlockIds.CHORUS_PLANT] = ChorusPlant
            #             self.list[BlockIds.INVISIBLE_BEDROCK] = InvisibleBedrock

            for id, clas in self.list:
                if clas is not None:
                    block = clas()

                    data = 0
                    while data < 16:
                        self.fullList[(id << 4) | data] = clas(data)
                        data += 1

                    self.solid[id] = block.isSolid()
                    self.transparent[id] = block.isTransparent()

    def get(self, id, meta=0, pos: Position = None):
        try:
            block = self.list[id]
            if block is not None:
                block = block(meta)
            else:
                block = UnknownBlock(id, meta)
        except RuntimeError:
            block = UnknownBlock(id, meta)

        if pos is not None:
            block.x = pos.x
            block.y = pos.y
            block.z = pos.z
            block.level = pos.level

    def __init__(self, id, meta=0):
        self.id = int(id)
        self.meta = int(meta)

    def place(self, item: Item, block: Block, target: Block, face, fx, fy, fz, player: Player = None):
        return self.getLevel().setBlock(self, self, True, True)

    def isBreakable(self, item: Item):
        return True

    def onBreak(self, item: Item):
        return self.getLevel().setBlock(self, Air, True, True)

    def onUpdate(self, type):
        return False

    def onActivate(self, item: Item, player: Player = None):
        return False

    def getHardness(self):
        return 10

    def getResistance(self):
        return self.getHardness() * 5

    def getToolType(self):
        return Tool.TYPE_NONE

    def getFrictionFactor(self):
        return 0.6

    def getLightLevel(self):
        return 0

    def canBePlaced(self):
        return True

    def canBeReplaced(self):
        return False

    def isTransparent(self):
        return False

    def isSolid(self):
        return True

    def canBeFlowedInto(self):
        return False

    def canBeActivated(self):
        return False

    def hasEntityCollision(self):
        return False

    def canPassThrough(self):
        return False

    def getName(self):
        return "Unknown"

    def getId(self):
        return self.id

    def addVelocityToEntity(self, entity: Entity, vector: Vector3):
        pass

    def getDamage(self):
        return self.meta

    def setDamage(self, meta):
        self.meta = meta & 0x0f

    def position(self, v: Position):
        self.x = int(v.x)
        self.y = int(v.y)
        self.z = int(v.z)
        self.level = v.level
        self.boundingBox = None

    def getDrops(self, item: Item):
        if not isset(self.list[self.getId()]):
            return {}
        else:
            return {[self.getId(), self.getDamage(), 1], }

    def getBreakTime(self, item: Item):
        base = self.getHardness() * 1.5
        if self.canBeBrokenWith(item):
            if self.getToolType() == Tool.TYPE_SHEARS and item.isShears():
                base /= 15
