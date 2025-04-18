from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status


class GenericModelViewSet(ModelViewSet):
    def format_response(
            self, data=None, message="OK", success=True, meta=None, status_code=status.HTTP_200_OK
    ):
        response = {
            "success": success,
            "message": message,
            "data": data if isinstance(data, list) else [data] if data else [],
        }
        if meta is not None:
            response["meta"] = meta
        return Response(response, status=status_code)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 直接取用paginator的資訊，而非包裝過的Response
            pagination_meta = {
                "total_count": self.paginator.page.paginator.count,
                "total_pages": self.paginator.page.paginator.num_pages,
                "current_page": self.paginator.page.number,
                "page_size": self.paginator.get_page_size(request),
            }
            return self.format_response(
                data=serializer.data,
                meta=pagination_meta,
            )

        serializer = self.get_serializer(queryset, many=True)
        return self.format_response(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.format_response(data=[serializer.data])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return self.format_response(
            data=[serializer.data], status_code=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.format_response(data=[serializer.data])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.format_response(
            data=[], message="Deleted", status_code=status.HTTP_204_NO_CONTENT
        )
