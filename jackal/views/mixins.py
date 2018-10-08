from views.generics import BaseDetailUpdateDestroyGeneric, BaseListCreateGeneric, PaginateListGeneric, SimpleGeneric


class DetailMixin(BaseDetailUpdateDestroyGeneric):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)


class DestroyMixin(BaseDetailUpdateDestroyGeneric):
    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class UpdateMixin(BaseDetailUpdateDestroyGeneric):
    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)


class DetailUpdateMixin(BaseDetailUpdateDestroyGeneric):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)

    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)


class DetailUpdateDestroyMixin(BaseDetailUpdateDestroyGeneric):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)

    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class DetailDestroyMixin(BaseDetailUpdateDestroyGeneric):
    def get(self, request, **kwargs):
        return self.detail(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class UpdateDestroyMixin(BaseDetailUpdateDestroyGeneric):
    def patch(self, request, **kwargs):
        return self.update(request, **kwargs)

    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)


class ListMixin(BaseListCreateGeneric):
    def get(self, request, **kwargs):
        return self.list(request, **kwargs)


class CreateMixin(BaseListCreateGeneric):
    def post(self, request, **kwargs):
        return self.create(request, **kwargs)


class ListCreateMixin(BaseListCreateGeneric):
    def get(self, request, **kwargs):
        return self.list(request, **kwargs)

    def post(self, request, **kwargs):
        return self.create(request, **kwargs)


class PaginateListMixin(PaginateListGeneric):
    def get(self, request, **kwargs):
        return self.paginated_list(request, **kwargs)


class PostMixin(SimpleGeneric):
    def post(self, request, **kwargs):
        return self.wrapper(request, method='post', **kwargs)


class GetMixin(SimpleGeneric):
    def get(self, request, **kwargs):
        return self.wrapper(request, method='get', **kwargs)


class PutMixin(SimpleGeneric):
    def put(self, request, **kwargs):
        return self.wrapper(request, method='put', **kwargs)


class PatchMixin(SimpleGeneric):
    def patch(self, request, **kwargs):
        return self.wrapper(request, method='patch', **kwargs)


class DeleteMixin(SimpleGeneric):
    def delete(self, request, **kwargs):
        return self.wrapper(request, method='delete', **kwargs)
