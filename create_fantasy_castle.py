#!/usr/bin/env python3
"""
🎮 EJEMPLO PRÁCTICO - MCP WORLD EDITOR
Demuestra cómo crear un conjunto completo de ubicaciones, objetos y eventos
usando el nuevo sistema estandarizado
"""

import asyncio
from mcp_world_editor import (
    MCPWorldEditor, 
    quick_location, 
    quick_object, 
    quick_event,
    LocationTemplate,
    ObjectTemplate,
    EventTemplate
)

async def create_fantasy_castle():
    """Crea un castillo de fantasía completo con MCP"""
    print("🏰 CREANDO CASTILLO DE FANTASÍA CON MCP")
    print("=" * 50)
    
    # Inicializar editor
    editor = MCPWorldEditor("adventure_world.db")  # Usar la BD principal del juego
    if not await editor.initialize():
        return
    
    created_locations = {}
    created_objects = {}
    created_events = {}
    
    # === UBICACIONES ===
    print("\n🏛️ Creando ubicaciones...")
    
    # 1. Entrada del castillo (ya existe pero la recreamos como ejemplo)
    entrance = quick_location(
        name="Entrada del Castillo Real",
        description="Majestuosas puertas de roble reforzadas con hierro se alzan ante ti. Escudos heráldicos decoran las columnas de mármol.",
        theme="castle",
        connections={"norte": "hall_principal", "sur": "camino_bosque", "este": "torre_guardia"},
        atmosphere="imponente y ceremonial"
    )
    
    success, entrance_id = await editor.create_location_with_mcp(entrance)
    if success:
        created_locations["entrance"] = entrance_id
        print(f"✅ Entrada creada: {entrance_id}")
    
    # 2. Torre de guardia
    guard_tower = quick_location(
        name="Torre de Guardia",
        description="Una alta torre circular con ventanas estrechas. Desde aquí se vigilan los caminos que llevan al castillo.",
        theme="castle",
        connections={"oeste": entrance_id, "arriba": "sala_armas"},
        atmosphere="vigilante y defensivo"
    )
    
    success, tower_id = await editor.create_location_with_mcp(guard_tower)
    if success:
        created_locations["tower"] = tower_id
        print(f"✅ Torre creada: {tower_id}")
    
    # 3. Sala de armas (arriba de la torre)
    armory = quick_location(
        name="Sala de Armas",
        description="Las paredes están cubiertas de armaduras, espadas, escudos y ballestas. El aire huele a aceite de armas y cuero.",
        theme="castle",
        connections={"abajo": tower_id},
        atmosphere="marcial y ordenado"
    )
    
    success, armory_id = await editor.create_location_with_mcp(armory)
    if success:
        created_locations["armory"] = armory_id
        print(f"✅ Sala de armas creada: {armory_id}")
    
    # === OBJETOS ===
    print("\n📦 Creando objetos temáticos...")
    
    # 1. Espada élfica en la sala de armas
    elven_sword = quick_object(
        name="Espada Élfica Brillante",
        description="Una elegante espada de hoja curva con runas élficas grabadas. La empuñadura está decorada con gemas que brillan suavemente.",
        location_id=armory_id,
        object_type="weapon"
    )
    elven_sword.properties = {
        "damage": 25,
        "durability": 150,
        "material": "mithril",
        "enchantment": "light_blessing",
        "rarity": "legendary"
    }
    elven_sword.ai_context = "Arma élfica antigua con bendición de luz. Efectiva contra criaturas de la oscuridad."
    
    success, sword_id = await editor.create_object_with_mcp(elven_sword)
    if success:
        created_objects["elven_sword"] = sword_id
        print(f"✅ Espada élfica creada: {sword_id}")
    
    # 2. Escudo del guardián en la torre
    guardian_shield = quick_object(
        name="Escudo del Guardián Real",
        description="Un sólido escudo de acero con el emblema real grabado. Muestra signos de haber visto muchas batallas.",
        location_id=tower_id,
        object_type="weapon"  # Los escudos son equipo de combate
    )
    guardian_shield.properties = {
        "defense": 15,
        "durability": 120,
        "material": "steel",
        "weight": 8.5,
        "history": "royal_guard"
    }
    guardian_shield.is_usable = True
    guardian_shield.ai_context = "Escudo ceremonial que ofrece protección considerable. Símbolo de autoridad real."
    
    success, shield_id = await editor.create_object_with_mcp(guardian_shield)
    if success:
        created_objects["shield"] = shield_id
        print(f"✅ Escudo creado: {shield_id}")
    
    # 3. Llave dorada en la entrada
    golden_key = quick_object(
        name="Llave Dorada del Chambelán",
        description="Una ornamentada llave de oro con el sello real. Abre las habitaciones privadas del castillo.",
        location_id=entrance_id,
        object_type="treasure"
    )
    golden_key.properties = {
        "material": "gold",
        "opens": ["royal_chambers", "treasure_room", "secret_passage"],
        "value": 500,
        "authority_level": "high"
    }
    golden_key.is_hidden = True  # Necesita ser buscada
    golden_key.ai_context = "Llave maestra que abre áreas restringidas del castillo. Muy valiosa para la exploración."
    
    success, key_id = await editor.create_object_with_mcp(golden_key)
    if success:
        created_objects["golden_key"] = key_id
        print(f"✅ Llave dorada creada: {key_id}")
    
    # === EVENTOS ===
    print("\n⚡ Creando eventos interactivos...")
    
    # 1. Evento de entrada al castillo
    castle_entrance_event = quick_event(
        name="Entrada Majestuosa",
        description="Evento al entrar al castillo por primera vez",
        trigger_type="location_enter",
        trigger_condition=entrance_id,
        action_type="message",
        action_data={
            "message": "Las enormes puertas se abren con un eco profundo. Guardias fantasma parecen observarte desde las sombras de las columnas.",
            "mood": "majestic",
            "sound_effect": "heavy_doors",
            "first_time_only": True
        }
    )
    
    success, entrance_event_id = await editor.create_event_with_mcp(castle_entrance_event)
    if success:
        created_events["entrance"] = entrance_event_id
        print(f"✅ Evento de entrada creado: {entrance_event_id}")
    
    # 2. Evento al usar la espada élfica
    sword_use_event = quick_event(
        name="Despertar de la Espada Élfica",
        description="Evento al tomar la espada élfica por primera vez",
        trigger_type="object_use",
        trigger_condition=sword_id,
        action_type="message",
        action_data={
            "message": "Al tomar la espada, las runas élficas brillan intensamente y sientes una corriente de poder ancestral recorrer tus brazos.",
            "mood": "mystical", 
            "temporary_effect": "enhanced_strength",
            "duration": 300  # 5 minutos
        },
        is_repeatable=False
    )
    
    success, sword_event_id = await editor.create_event_with_mcp(sword_use_event)
    if success:
        created_events["sword_awakening"] = sword_event_id
        print(f"✅ Evento de espada creado: {sword_event_id}")
    
    # 3. Evento de descubrimiento de llave oculta
    key_discovery_event = quick_event(
        name="Descubrimiento de la Llave Dorada",
        description="Evento al encontrar la llave oculta",
        trigger_type="command",
        trigger_condition="buscar llave|examinar entrada|search key",
        action_type="spawn_object",
        action_data={
            "object_id": key_id,
            "reveal_message": "¡Al examinar cuidadosamente las columnas, encuentras una llave dorada escondida tras el escudo heráldico!",
            "location_id": entrance_id
        },
        is_repeatable=False
    )
    
    success, key_event_id = await editor.create_event_with_mcp(key_discovery_event)
    if success:
        created_events["key_discovery"] = key_event_id
        print(f"✅ Evento de descubrimiento creado: {key_event_id}")
    
    # === RESUMEN ===
    print(f"\n📊 CASTILLO COMPLETADO:")
    print(f"   🏛️ Ubicaciones creadas: {len(created_locations)}")
    print(f"   📦 Objetos creados: {len(created_objects)}")
    print(f"   ⚡ Eventos creados: {len(created_events)}")
    
    # Mostrar IDs para referencia
    print(f"\n🆔 IDs de referencia:")
    for name, location_id in created_locations.items():
        print(f"   {name}: {location_id}")
    
    # Exportar todo
    export_file = await editor.export_templates_to_json("castle_fantasy_templates.json")
    print(f"\n💾 Castillo exportado a: {export_file}")
    
    # Mostrar contexto MCP de una ubicación
    print(f"\n🔍 Contexto MCP de la Sala de Armas:")
    if armory_id:
        context = await editor.mcp_provider.generate_world_context_for_ai(
            armory_id,
            query="espada élfica"
        )
        print(context)
    
    editor.close()
    print(f"\n✅ Castillo de fantasía creado exitosamente!")
    print(f"🎮 Puedes probarlo ejecutando: python start_ai_game.py")

if __name__ == "__main__":
    asyncio.run(create_fantasy_castle())
