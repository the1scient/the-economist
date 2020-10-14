import random
import discord
import urllib
import secrets
import asyncio
import aiohttp
import re
import requests
import json


from selenium import webdriver
import time
from io import BytesIO
from discord.ext import commands
from utils import lists, permissions, http, default, argparser
from requests_html import HTMLSession



class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("economist.json")

    @commands.command(aliases=['cotação', 'pricequote'])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def cotacao(self, ctx, *, search: commands.clean_content):
        """[PT] Retorna uma cotação desejada // [EN] Returns a desired price quote. \n Usagem: $cotacao MOEDA-BRL \n Lista:  $cotlista"""
        async with ctx.channel.typing():
            message = await ctx.send("<a:loading:732671405816152105> Carregando resultados :dollar:")
            url = f'https://economia.awesomeapi.com.br/'+ search +'/?format=json'
            response = requests.get(url, verify=True) 
            data = response.json()
            high = float(data[0]["high"])
            if "status" in data:
                await ctx.send(":flag_br: Algo deu zika malandro")
        high = "{:,.2f}".format(high)
        await message.edit(content="<:verificacao:732675855440019538> **Busca realizada**! \n Cotação de *{0}*: **R${1}**".format(search, high))
            
    @commands.command(aliases=['pqlist'])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def cotlista(self, ctx):
        """[PT] Retorna uma cotação desejada // [EN] Returns a desired price quote. \n Usagem: $cotacao MOEDA-BRL \n Lista:  $cotlista"""
        async with ctx.channel.typing():
             message = await ctx.send("<a:loading:732671405816152105> Carregando resultados de lista...")
             embedVar = discord.Embed(title="Lista de Cotações", color=0x00ff00)
        embedVar.set_thumbnail(url=ctx.bot.user.avatar_url)
        embedVar.add_field(name="USD-BRL", value="Dólar Comercial", inline=True)
        embedVar.add_field(name="USDT-BRL", value="Dólar Turístico", inline=True)
        embedVar.add_field(name="CAD-BRL", value="Dólar Canadense", inline=True)
        embedVar.add_field(name="AUD-BRL", value="Dólar Australiano", inline=True)
        embedVar.add_field(name="EUR-BRL", value="Euro", inline=True)
        embedVar.add_field(name="GBP-BRL", value="Libra Esterlina", inline=True)
        embedVar.add_field(name="ARS-BRL", value="Peso Argentino", inline=True)
        embedVar.add_field(name="JPY-BRL", value="Iene Japonês", inline=True)
        embedVar.add_field(name="CHF-BRL", value="Franco Suíço", inline=True)
        embedVar.add_field(name="CNY-BRL", value="Yuan Chinês", inline=True)
        embedVar.add_field(name="YLS-BRL", value="Novo Shekel Israelense", inline=True)
        embedVar.add_field(name="BTC-BRL", value="Bitcoin", inline=True)
        embedVar.add_field(name="LTC-BRL", value="Litecoin", inline=True)
        embedVar.add_field(name="ETH-BRL", value="Ethereum", inline=True)
        embedVar.add_field(name="XRP-BRL", value="Ripple", inline=True)
        await message.edit(embed=embedVar, content="<:verificacao:732675855440019538> Busca realizada, exibindo um total de 15 resultados.")
                
    @commands.command(aliases=['ação', 'action'])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def acao(self, ctx, *, search: commands.clean_content):
        """[PT] Retorna uma ação desejada // [EN] Returns a desired price quote. \n Usagem: $acao AÇÃO (ex BIDI4) \n Lista:  $acaolista"""
        async with ctx.channel.typing():
            message = await ctx.send("<a:loading:732671405816152105> Carregando resultados :dollar:")
            url = 'https://api.hgbrasil.com/finance/stock_price?key=7f0fe464&symbol='+ search
            response = requests.get(url, verify=True) 
            data = response.json()
            name = data["results"][search]["name"]
            region_raw = data["results"][search]["region"]
            region = region_raw.replace("Sao Paolo", "São Paulo")
            currency = data["results"][search]["currency"]
            price = data["results"][search]["price"]
            atualizacao = data["results"][search]["updated_at"]
            opentime = data["results"][search]["market_time"]["open"]
            closetime = data["results"][search]["market_time"]["close"]
            embedVar = discord.Embed(title=name + " - Informações de Ação", color=0x00ff00)
            embedVar.set_thumbnail(url="https://image.shutterstock.com/image-photo/stock-forex-trading-indicator-on-260nw-1720647160.jpg")
            embedVar.add_field(name="Nome", value=name)
            embedVar.add_field(name="Região", value=region)
            embedVar.add_field(name="Moeda", value=currency)
            embedVar.add_field(name="Preço", value="R${:,.2f}".format(price))
            embedVar.add_field(name="Abertura", value=opentime)
            embedVar.add_field(name="Fechamento", value=closetime)
            embedVar.add_field(name="Última atualização", value=atualizacao)
            embedVar.add_field(name="Gráfico TradingView", value="https://br.tradingview.com/symbols/BMFBOVESPA-"+search+"/")


                
        await message.edit(content="<:verificacao:732675855440019538> **Busca realizada**! Exibindo resultados. \n", embed=embedVar)
       
    @commands.command(aliases=['argumentos', 'a'])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def args(self, ctx, arg1, arg2):
        """[PT] Retorna argumentos digitados"""
        async with ctx.channel.typing():
        
            await ctx.send("Você enviou {} e {}".format(arg1, arg2))
                
    @commands.command(aliases=['conversao', 'conversão'])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def converter(self, ctx, arg1, arg2):
        """[PT] Converte uma determinada moeda da Lista de Cotações ($cotlista) para BRL. \n Ex: $converter USD-BRL 1"""
        async with ctx.channel.typing():
            message = await ctx.send("<a:loading:732671405816152105> Carregando resultados :dollar:")
            url = f'https://economia.awesomeapi.com.br/'+ arg1 +'/?format=json'
            response = requests.get(url, verify=True) 
            data = response.json()
            high = data[0]["high"]
            
            if len(arg2) > 30:
                await message.edit(content="<:cursed:734961757084188763> Envie um número menor, por favor!")
            else:
                qt = float(arg2)
                high = float(high)
                res = high * qt
                res = "R${:,.2f}".format(res)
                await message.edit(content="<:verificacao:732675855440019538> **Busca realizada**! Exibindo resultados... \n Conversão: {0}".format(res))


def setup(bot):
    bot.add_cog(Economia(bot))
