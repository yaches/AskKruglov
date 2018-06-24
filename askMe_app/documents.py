from django_elasticsearch_dsl import DocType, Index
from elasticsearch_dsl import analyzer, tokenizer
from .models import Question, Answer

askme = Index('askme')

askme.settings(
    number_of_shards=1,
    number_of_replicas=0
)

my_analyzer = analyzer('my_analyzer',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
)

askme.analyzer(my_analyzer)

@askme.doc_type
class QuestionDocument(DocType):
    class Meta:
        model = Question 

        fields = [
            'title',
            'text',
        ]
