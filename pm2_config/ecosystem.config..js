module.exports = {
  deploy : {
    production : {
      user : 'isla',
      host : '192.168.1.110',
      ref  : 'origin/master',
      repo : 'git@git.vmo.dev:global/vmo-devops-internal/fresher-project/sonpv-project.git',
      path : '/home/isla/flask_blog',
      'post-deploy': 'cd /home/isla/flask_blog/current ; source venv/bin/activate; pm2 restart ecosystem_run.json',
      'pre-setup': 'rm -rf /home/isla/flask_blog/*',
      'post-setup' : 'cd /home/isla/flask_blog/current; python3 -m venv venv; source venv/bin/activate; pip3 install -r requirements.txt; sudo ufw allow 5000; sudo ufw reload; pm2 start ecosystem_run.json --env prod'
    }
  }
};
