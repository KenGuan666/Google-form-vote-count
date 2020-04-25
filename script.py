import csv

whitelist_emails = set()

# string constants
email = 'email'
name = 'name'
role = 'role'
zx = '主席'
cw = '财务部部长'
hd = '活动部部长'
gg = '公关部部长'
ms = '秘书长'
xx = '信息技术部部长'
wy = '文艺部部长'
xs = '学术部部长'
zy = '职业发展部部长'
vote_yes = '支持'
vote_no = '反对'
board = '主席团'

roles = [zx, cw, hd, gg, ms, xx, wy, xs, zy]

whitelist_format = {
    email: 1,
}

vote_format = {
    email: 1,
    name: 2,
    role: 4,
    zx: 5,
    cw: 6,
    hd: 7,
    gg: 8,
    ms: 9,
    xx: 10,
    wy: 11,
    xs: 12,
    zy: 13,
}

yes_no_positions = {
    cw: '包义博',
    hd: '樊一丁',
    xx: '刘梓郁 Hanson',
}

vote_counts = {
    zx: {
        '阚杰元 Ken': 0,
        '尹逸菲': 0,
        '李嘉琳 Jessamine': 0,
    },
    cw: {
        vote_yes: 0,
        vote_no: 0,
    },
    hd: {
        vote_yes: 0,
        vote_no: 0,
    },
    gg: {
        '古峻宇 Edward': 0,
        '杨致远 Mark': 0,
    },
    ms: {
        '黄小桑 Birdy': 0,
        '邵蕾 Amber': 0,
    },
    xx: {
        vote_yes: 0,
        vote_no: 0,
    },
    wy: {
        '韩梦雨 Ruby': 0,
        '朱明雨 Helen': 0,
    },
    xs: {
        '罗纪泽': 0,
        '田薏歆 Yixin': 0,
    },
    zy: {
        '丁周节 Jason': 0,
        '王若沣 Edison': 0,
        '张任莹': 0,
    },
}

invalid_email_address_votes = set()
repeated_votes = set()
voted_emails = set()
effective_votes = set()

def parse_vote(row):
    _name = row[vote_format[name]]
    _email = row[vote_format[email]]
    _role = row[vote_format[role]]
    vote_repr = (_name, _email)

    weight = 5 if _role == board else 1
    
    if not _email:
        return
    if _email not in whitelist_emails:
        invalid_email_address_votes.add(vote_repr)
        return
    if _email in voted_emails:
        repeated_votes.add(vote_repr)
        return
    
    effective_votes.add(_email)
    for r in roles:
        _vote = row[vote_format[r]]
        if _vote:
            vote_counts[r][_vote] += weight

def parse_results():
    for r, v in vote_counts.items():
        print('{}:'.format(r))
        if r in yes_no_positions:
            print('   {}, {}: {}, {}: {}.'.format(yes_no_positions[r], vote_yes, v[vote_yes], vote_no, v[vote_no]))
        else:
            for candidate, counts in v.items():
                print('   {}, {}.'.format(candidate, counts))
    
    print('有效投票: {}份.'.format(len(effective_votes)))
    print('无效投票:')
    if not invalid_email_address_votes:
        print('   无.')
    else:
        for _name, _email in invalid_email_address_votes:
            print('   {}, {}'.format(_name, _email))
    print('重复投票:')
    if not repeated_votes:
        print('   无.')
    else:
        for _name, _email in repeated_votes:
            print('   {}, {}'.format(_name, _email))

with open('whitelist.csv', newline='') as whitelist:
    reader = csv.reader(whitelist)
    for row in reader:
        _email = row[whitelist_format[email]].strip().lower()
        if _email:
            whitelist_emails.add(_email)
            if not _email.split('@')[1] == ('berkeley.edu'):
                print(_email)

with open('votes.csv', newline='') as votes:
    reader = csv.reader(votes)
    for row in reader:
        parse_vote(row)

parse_results()
