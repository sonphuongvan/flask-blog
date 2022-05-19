module.exports = {
  deploy : {
    production : {
      user : 'isla',
      host : '172.16.2.95',
      ref  : 'origin/master',
      repo : 'git@git.vmo.dev:global/vmo-devops-internal/fresher-project/sonpv-project.git',
      path : '/home/isla',
      'pre-deploy-local': '',
      'post-deploy' : 'touch /tmp/test.txt',
      'pre-setup': ''
    }
  }
};
