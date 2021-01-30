from aiohttp import web
from objects import glob

from objects.score import Score, SubmissionStatus

import helpers, logging, copy, aiofiles

# i fucking hate this part
# also code is abit retarded so might change later
async def submit_score(request):
    ''' retarded score submission god someone help me i fucking hate coding '''
    params = await helpers.readParam(request)
    p = await glob.players.get(id=int(params['userID']))

    # verify sign thing... nvm what 
    # print(p.sign, params['sign'])

    if not p:
        return web.Response(text='FAILED\nWho the fuck are you lol')


    if (mapHash := params.get('hash')):
        p.stats.playing = mapHash
        logging.debug(f'changed {p} playing to {mapHash}')
        return web.Response(text=f'SUCCESS\n1 {p.id}')

    elif playData := params.get('data'):
        s = await Score.from_submission(playData)

        if not s:
            # logging.debug('shit wtf')
            # pretty sure this one just crash the client
            return 'FAILED\nfucked'

        if s.status == SubmissionStatus.BEST:
            # fuck off other score into status 1 (submitted)
            await glob.db.execute('UPDATE scores SET status = 1 WHERE status = 2 AND mapHash = ? AND playerID = ?', [s.mapHash, s.player.id])

        vals = [s.status, s.mapHash, s.player.id, s.score, s.max_combo, s.grade, s.acc, s.h300, s.hgeki, s.h100, s.hkatsu, s.h50, s.hmiss, s.mods, s.pp]
        s.id = await glob.db.execute('INSERT INTO scores VALUES (NULL, ?, NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', vals)


        """ pain and suffering """
        upload_replay = False
        if s.status == SubmissionStatus.BEST:
            upload_replay = True


        # update stats
        stats = s.player.stats
        prev_stats = copy.copy(stats)

        # mmm
        stats.plays += 1
        stats.tscore += s.score

        if s.status == SubmissionStatus.BEST:
            additive = s.score
            ppadd = s.pp

            if s.prev_best:
                additive -= s.prev_best.score

            stats.rscore += additive

        # update stats
        await glob.db.execute(
            'UPDATE stats SET rscore = ?, tscore = ?, plays = ? where id = ?',
            [stats.rscore, stats.tscore, stats.plays, s.player.id]
        )

        # aight we for sure know that the entire thing is fine and k00l so update stats
        await s.player.update_stats()


        # fuck my ass i hope this works
        res = f'SUCCESS\n{int(stats.rank)} {int(stats.pp) if glob.config.pp else int(stats.rscore)} {stats.droid_acc} {s.rank} {s.id if upload_replay else ""}'
        return web.Response(text=res)




        

    return web.Response(text='FAILED\nFUCK')