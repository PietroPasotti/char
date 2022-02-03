#!/usr/bin/env python3
# Copyright 2022 pietro
# See LICENSE file for licensing details.

import logging
import os
import random
import requests

import httpx
from fastapi import FastAPI, BackgroundTasks, Request

app = FastAPI()
logger = logging.getLogger('char')
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)


@app.on_event("startup")
def startup():
    app.state.hp = random.randrange(40, 60)
    enemies = os.environ.get('ENEMIES', '')
    logger.debug(f"Enemies: {enemies}")
    name = os.environ.get('NAME', '')
    logger.info(f'spawning {name}...')
    app.state.name = name
    app.state.enemies = enemies.split(';') if enemies else []


async def try_ping(enemy):
    client: httpx.AsyncClient
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get('http://' + enemy + '/is_alive')
            return resp.is_success and resp.json()
    except Exception as e:
        logger.error(f"{e}; cannot ping {enemy}")
        return False


@app.get('/is_alive')
async def is_alive():
    """is this character alive?"""
    return app.state.hp > 0


@app.get('/status')
async def status(request: Request):
    """returns the hp of this instance and a list of known enemies
    (and whether they're still alive)
    """
    return {
        'name': app.state.name or str(request.client.host),
        'hp': app.state.hp,
        'enemies':
            {enemy: await try_ping(enemy) for enemy in app.state.enemies}
    }


# async def async_retaliate(enemies):
#     for enemy in enemies:
#         damage = random.randrange(10, 20)
#         async with httpx.AsyncClient() as client:
#             logger.info(f'dealing {damage} to {enemy}')
#             url = 'http://' + enemy + f'/attack?damage={damage}'
#             try:
#                 await client.post(url)
#             except Exception as e:
#                 logger.error(f"{e}: cannot deal damage to {enemy}")


def retaliate(enemies):
    for enemy in enemies:
        damage = random.randrange(10, 20)
        logger.info(f'dealing {damage} to {enemy}')
        url = 'http://' + enemy + f'/attack?damage={damage}'
        try:
            requests.post(url)
        except Exception as e:
            logger.error(f"{e}: cannot deal damage to {enemy}")


@app.post("/attack")
async def attack(damage: int, background_tasks: BackgroundTasks):
    """inflicts `damage` to this char; the char will attack back!"""
    app.state.hp -= damage
    logger.info(f'taken {damage}')

    if app.state.hp <= 0:
        logger.info('char is dead')
    elif not (enemies := app.state.enemies):
        logger.info('nobody to leash out to')
    else:
        logger.info('retaliating')
        # background_tasks.add_task(async_retaliate, enemies)
        background_tasks.add_task(retaliate, enemies)
    return app.state.hp


@app.post("/heal")
async def attack(damage: int):
    """Heals this char."""
    app.state.hp = random.randrange(40, 60)
