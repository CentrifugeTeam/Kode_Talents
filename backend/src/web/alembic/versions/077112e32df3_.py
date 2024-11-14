"""empty message

Revision ID: 077112e32df3
Revises: 446c1283e739
Create Date: 2024-10-30 17:00:49.557132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy

from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from app.db.models.users import User
from app.db.models.questions import Question, Speciality
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory


class Factory(SQLAlchemyFactory):
    __is_base_factory__ = True
    __set_relationships__ = False


# revision identifiers, used by Alembic.
revision: str = '077112e32df3'
down_revision: Union[str, None] = '446c1283e739'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('specialities',
                    sa.Column('name', sa.String(length=300), nullable=False),
                    sa.Column('text', sa.String(), nullable=False),
                    sa.Column('urls', sa.String(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('questions',
                    sa.Column('name', sa.String(length=300), nullable=False),
                    sa.Column('speciality_id', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['speciality_id'], ['specialities.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    # ### end Alembic commands ###
    async def seed_db(connection: AsyncConnection):
        session = AsyncSession(bind=connection, expire_on_commit=False)
        design = Speciality(name='designer', text="""В своих решения дизайнер основывается на исследовании привычек, культурных предпочтений и стремлений людей. Также дизайнер сопровождает продукт пока тот врастает в рынок и помогает собирать обратную связь о повышении качества жизни и делать выводы о следующих шагах в развитии.
Дизайнер – социальный игрок, его поле борьбы за качество – опыт клиентов. Именно дизайнер помогает инженерам собрать культурный контекст, реальную потребительную среду в которой живут пользователи, выяснить текущий опыт людей, выявить барьеры и предложить наилучшее решение с учетом окружения клиентов.""",
                            urls="https://ux-journal.ru/dizajner-v-it-zachem-on-nuzhen-i-kak-im-stat.html;https://ru.wikipedia.org/wiki/%D0%94%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD")
        backend = Speciality(name='backend', text="""Бэкенд-разработчик (backend developer) — это специалист, который занимается серверной частью сайтов, мобильных и десктопных приложений и игр. Он реализует внутреннюю логику работы приложения, обеспечивает его взаимодействие с базами данных и внешними сервисами.

По другую сторону сервера задачи решают фронтенд-разработчики. Они отвечают за клиентскую часть продукта: вёрстку, работу и взаимодействие элементов интерфейса, внешний вид данных и так далее. В общем, за всё, что пользователи видят на своих экранах.""", urls='https://skillbox.ru/media/code/bekendrazrabotchik-kto-eto-chem-on-zanimaetsya-i-kak-im-stat/')
        frontend = Speciality(name='frontend', text="""FrontEnd разработчик создает видимую для пользователя часть веб-страницы и его главная задача – точно передать в верстке то, что создал дизайнер, а также реализовать пользовательскую логику.

Для того, чтобы стать FrontEnd разработчиком, не нужны знания математики. Освоить специальность Вы сможете за 3-6 месяцев, в зависимости от того, сколько времени будете уделять теории и кодингу. Наша программа обучения выверена на практике и включает в себя самые необходимые и современные технологии""", urls='https://rabota.sber.ru/media/kak-stat-frontend-razrabotchikom/')
        specs = [design, backend, frontend]
        for spec in specs:
            session.add(spec)
            await session.commit()



        seeds = [{1: ('Работать над созданием приложений с виртуальной или дополненной реальностью', design),
                  2: ('Делать красивые и аккуратные сайты из дизайн-макетов', design),
                  3: ('Делать важную, но малозаметную работу: оптимизировать, настраивать и обеспечивать надёжность сайта', backend),
                  4: ('Искать ошибки и придумывать способы, как лучше их исправить', backend)},
                 {1: ('Создавать плавные переходы и интересные анимации в мобильном приложении', frontend),
                  2: ('Придумывать новые и нетривиальные способы поиска ошибок', backend),
                  3: ('Программировать сайты так, чтобы на любых устройствах они отображались корректно', frontend),
                  4: ('Разносторонне продумывать логику и внутреннюю структуру будущей программы', backend)},
                 {1: ('Делать мобильное приложение удобным и понятным для пользователя', design),
                  2: ('Делать сайты удобными и понятными для пользователей', design),
                  3: ('Быть специалистом, от внимания которого не ускользнёт ни один сдвинутый пиксель', design),
                  4: ('Уметь делать всю работу целиком,от идеи и до последней строчки кода', design)},
                 {1: ('Активно использовать в программировании микрофон, камеру, геолокацию и другие функции',frontend),
                  2: ('Придумывать программы, которые автоматически ищут ошибки', backend),
                  3: ('Уметь одинаково хорошо настраивать операционные системы и разрабатывать сайты', backend),
                  4: ('Делать сайты удобными для людей с ограниченными возможностями', frontend)},
                 {1: ('Работать над программированием новых фишек мобильного приложения', frontend),
                  2: ('Создавать интересные эффектыи анимации на сайте ', design),
                  3: ('Разбираться во всех областях программирования, пусть даже и поверхностно', backend),
                  4: ('Педантично, шаг за шагом, проверять правильность работы каждой детали', backend)}]
        for s in seeds:
            for _, values in s.items():
                q = Question(name=values[0])
                q.speciality_id = values[1].id
                session.add(q)
                await session.flush()
                await session.commit()

        # await u_factory.create_async(id=695473622, is_superuser=True)

    op.run_async(seed_db)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('questions')
    op.drop_table('specialities')
    # ### end Alembic commands ###