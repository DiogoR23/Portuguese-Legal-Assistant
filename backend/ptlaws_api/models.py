import uuid
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns

# Create your models here.
class Article(DjangoCassandraModel):
    id_articles = columns.UUID(primary_key=True, default=uuid.uuid4)
    url = columns.Text(required=True)
    title = columns.Text(required=True)
    content = columns.Text(required=True)

    class Meta:
        db_table = 'articles'
        keyspace = 'cassandra'


