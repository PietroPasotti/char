#!/usr/bin/env python3
# Copyright 2022 pietro
# See LICENSE file for licensing details.

import logging
import os
import random

import httpx
from fastapi import FastAPI

app = FastAPI()
logger = logging.getLogger('char')


@app.on_event("startup")
def startup():
    app.state.hp = random.randrange(40, 60)
    enemies = os.environ.get('ENEMIES', '')
    name = os.environ.get('NAME', '')
    logger.info(f'spawning {name}...')
    app.state.name = name
    app.state.enemies = enemies.split(';') if enemies else []


async def deal(enemy, damage, client: httpx.AsyncClient):
    await client.post('http://' + enemy + '/attack', data={'damage': damage})


async def try_ping(enemy):
    client: httpx.AsyncClient
    async with httpx.AsyncClient() as client:
        resp = await client.get('http://' + enemy + '/is_alive')
        return resp.is_success and resp.json()


@app.get('/is_alive')
async def is_alive():
    """is this character alive?"""
    return app.state.hp > 0


@app.get('/status')
async def status():
    """returns the hp of this instance and a list of known enemies (and whether they're still alive)
    """
    return {'name': app.state.name,
            'hp': app.state.hp,
            'enemies':
                {enemy: await try_ping(enemy) for enemy in app.state.enemies}
            }


@app.post("/attack")
async def attack(damage: int):
    """inflicts `damage` to this char; the char will attack back!"""
    if app.state.hp < 0:
        raise RuntimeError('dead')

    app.state.hp -= damage
    logger.info(f'taken {damage}')
    if app.state.hp > 0:
        dealt = random.randrange(10, 20)
        logger.info(app.state.enemies)
        for enemy in app.state.enemies:
            async with httpx.AsyncClient() as client:
                await deal(enemy, dealt, client)
                logger.info(f'dealt {damage} to {enemy}')
    else:
        logger.info(f'dead.')
    return app.state.hp
