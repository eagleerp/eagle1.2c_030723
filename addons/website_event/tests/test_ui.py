import eagle.tests


@eagle.tests.tagged('post_install', '-at_install')
class TestUi(eagle.tests.HttpCase):
    def test_admin(self):
        self.phantom_js("/", "eagle.__DEBUG__.services['web_tour.tour'].run('event')", "eagle.__DEBUG__.services['web_tour.tour'].tours.event.ready", login='admin')
